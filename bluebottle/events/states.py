from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from bluebottle.activities.states import ActivityStateMachine, ContributionStateMachine
from bluebottle.events.effects import SetTimeSpent, ResetTimeSpent
from bluebottle.events.messages import (
    EventSucceededOwnerMessage,
    EventRejectedOwnerMessage,
    ParticipantRejectedMessage,
    ParticipantApplicationMessage,
    ParticipantApplicationManagerMessage,
)
from bluebottle.events.models import Event, Participant
from bluebottle.follow.effects import (
    FollowActivityEffect, UnFollowActivityEffect
)
from bluebottle.fsm.effects import (
    TransitionEffect,
    RelatedTransitionEffect
)
from bluebottle.fsm.state import State, EmptyState, Transition
from bluebottle.notifications.effects import NotificationEffect


class EventStateMachine(ActivityStateMachine):
    model = Event
    submitted = State(
        _('Submitted'),
        'submitted',
        _('The event is ready to go online once the initiative has been approved.')
    )

    def is_full(self):
        "the event is full"
        return self.instance.capacity == len(self.instance.participants)

    def is_not_full(self):
        "the event is not full"
        return self.instance.capacity > len(self.instance.participants)

    def should_finish(self):
        "the end time has passed"
        return self.instance.current_end and self.instance.current_end < timezone.now()

    def should_start(self):
        "the start time has passed"
        return self.instance.start and self.instance.start < timezone.now() and not self.should_finish()

    def should_open(self):
        "the start time has not passed"
        return self.instance.start and self.instance.start > timezone.now()

    def has_participants(self):
        """there are participants"""
        return len(self.instance.participants) > 0

    def has_no_participants(self):
        """there are no participants"""
        return len(self.instance.participants) == 0

    full = State(_('Full'), 'full', _('The attendee limit is reached and people can’t join any more.'))
    running = State(_('Running'), 'running', _('The event is taking place and people can’t join any more.'))

    submit = Transition(
        [
            ActivityStateMachine.draft,
            ActivityStateMachine.needs_work,
            ActivityStateMachine.cancelled
        ],
        submitted,
        description=_('The event will be submitted for review.'),
        automatic=False,
        name=_('Submit'),
        conditions=[
            ActivityStateMachine.is_complete,
            ActivityStateMachine.is_valid,
            ActivityStateMachine.initiative_is_submitted
        ],
        effects=[
            TransitionEffect(
                'approve',
                conditions=[
                    ActivityStateMachine.initiative_is_approved,
                    should_open
                ]
            ),
            TransitionEffect(
                'expire',
                conditions=[should_start, has_no_participants]
            ),
            TransitionEffect(
                'expire',
                conditions=[should_finish, has_no_participants]
            ),
            TransitionEffect(
                'succeed',
                conditions=[should_finish, has_participants]
            ),
        ]
    )

    approve = Transition(
        [
            ActivityStateMachine.submitted,
            ActivityStateMachine.rejected
        ],
        ActivityStateMachine.open,
        name=_('Approve'),
        automatic=True,
        description=_("The event will be visible in the frontend and people can join the event."),
        effects=[
            RelatedTransitionEffect('organizer', 'succeed'),
            TransitionEffect(
                'expire',
                conditions=[should_start, has_no_participants]
            ),
            TransitionEffect(
                'expire',
                conditions=[should_finish, has_no_participants]
            ),
            TransitionEffect(
                'succeed',
                conditions=[should_finish, has_participants]
            ),
        ]
    )

    cancel = Transition(
        [
            ActivityStateMachine.draft,
            ActivityStateMachine.needs_work,
            ActivityStateMachine.open,
            running,
            full,
            submitted
        ],
        ActivityStateMachine.cancelled,
        name=_('Cancel'),
        description=_('Cancel if the event will not be executed. '
                      'The activity manager will not be able to edit the event and '
                      'it won’t show up on the search page in the front end. '
                      'The event will still be available in the back office and appear in your reporting.'),
        automatic=False,
        effects=[
            RelatedTransitionEffect('organizer', 'fail'),
            RelatedTransitionEffect('participants', 'fail')
        ]
    )

    lock = Transition(
        [
            ActivityStateMachine.open,
            ActivityStateMachine.succeeded
        ],
        full,
        name=_("Lock"),
        description=_("People can no longer join the event. Triggered when the attendee limit is reached.")
    )

    reopen = Transition(
        full,
        ActivityStateMachine.open,
        name=_("Reopen"),
        description=_("People can join the event again. Triggered when the number of attendees become less than the attendee limit.")
    )

    reschedule = Transition(
        [
            running,
            ActivityStateMachine.cancelled,
            ActivityStateMachine.succeeded
        ],
        ActivityStateMachine.open,
        name=_("Reschedule"),
        description=_("People can join the event again, because the date has changed."),
        effects=[
            RelatedTransitionEffect('participants', 'reset')
        ]
    )

    start = Transition(
        [
            ActivityStateMachine.open,
            full
        ],
        running,
        name=_("Start"),
        description=_("Start the event. Triggered when the start time passes.")
    )

    expire = Transition(
        [
            ActivityStateMachine.submitted,
            ActivityStateMachine.open,
            ActivityStateMachine.succeeded
        ],
        ActivityStateMachine.cancelled,
        name=_("Expire"),
        description=_("The event didn’t have any attendees before the start time and is cancelled.")
    )

    succeed = Transition(
        [
            full,
            running,
            ActivityStateMachine.open,
            ActivityStateMachine.rejected,
            ActivityStateMachine.cancelled
        ],
        ActivityStateMachine.succeeded,
        name=_("Succeed"),
        description=_("The event ends and the contributions are counted. Triggered when the event end time passes."),
        effects=[
            NotificationEffect(EventSucceededOwnerMessage),
            RelatedTransitionEffect('participants', 'succeed')
        ]
    )

    reject = Transition(
        [
            ActivityStateMachine.draft,
            ActivityStateMachine.needs_work,
            ActivityStateMachine.submitted
        ],
        ActivityStateMachine.rejected,
        name=_('Reject'),
        description=_('Reject in case this event doesn’t fit your program or the rules of the game. '
                      'The activity owner will not be able to edit the event and '
                      'it won’t show up on the search page in the front end. '
                      'The event will still be available in the back office and appear in your reporting.'),
        automatic=False,
        permission=ActivityStateMachine.is_staff,
        effects=[
            RelatedTransitionEffect('organizer', 'fail'),
            NotificationEffect(EventRejectedOwnerMessage),
        ]
    )

    restore = Transition(
        [
            ActivityStateMachine.rejected,
            ActivityStateMachine.cancelled,
            ActivityStateMachine.deleted,
        ],
        ActivityStateMachine.draft,
        name=_("Restore"),
        description=_("The status of the event is set to 'Draft'. The activity owner can edit the event again."),
        effects=[
            RelatedTransitionEffect('participants', 'reset'),
            RelatedTransitionEffect('organizer', 'reset')
        ]
    )


class ParticipantStateMachine(ContributionStateMachine):
    model = Participant

    withdrawn = State(
        _('Withdrawn'),
        'withdrawn',
        _("The person withdrew and will no longer attend the event.")
    )
    rejected = State(
        _('Rejected'),
        'rejected',
        _("The person was rejected and will not attend the event.")
    )
    no_show = State(
        _('No show'),
        'no_show',
        _("The person didn't attend the event and was marked absent.")
    )
    new = State(
        _('Joined'),
        'new',
        _("The person is attending the event.")
    )

    def is_user(self, user):
        """is the participant"""
        return self.instance.user == user

    def is_activity_owner(self, user):
        """is the activity manager or a staff member"""
        return user.is_staff or self.instance.activity.owner == user

    def event_will_become_full(self):
        "event will be full"
        activity = self.instance.activity
        return activity.capacity == len(activity.participants) + 1

    def event_will_become_open(self):
        "event will not be full"
        activity = self.instance.activity
        return activity.capacity == len(activity.participants)

    def event_is_finished(self):
        "event is finished"
        return self.instance.activity.current_end < timezone.now()

    def event_is_not_finished(self):
        "event is not finished"
        return not self.instance.activity.start < timezone.now()

    def event_will_be_empty(self):
        "event will be empty"
        return self.instance.activity.participants.exclude(id=self.instance.id).count() == 0

    initiate = Transition(
        EmptyState(),
        ContributionStateMachine.new,
        name=_("Join"),
        description=_("The person will be attending the event."),
        effects=[
            TransitionEffect(
                'succeed',
                conditions=[event_is_finished]
            ),
            RelatedTransitionEffect(
                'activity',
                'lock',
                conditions=[event_will_become_full]
            ),
            RelatedTransitionEffect(
                'activity',
                'succeed',
                conditions=[event_is_finished]
            ),
            NotificationEffect(ParticipantApplicationManagerMessage),
            NotificationEffect(ParticipantApplicationMessage),
            FollowActivityEffect,
        ]
    )
    withdraw = Transition(
        ContributionStateMachine.new,
        withdrawn,
        name=_('Withdraw'),
        description=_("The person will voluntarily cease to attend the event."),
        automatic=False,
        permission=is_user,
        effects=[
            RelatedTransitionEffect('activity', 'reopen', conditions=[event_will_become_open]),
            UnFollowActivityEffect
        ]
    )
    reapply = Transition(
        withdrawn,
        ContributionStateMachine.new,
        name=_('Join again'),
        description=_("The person will be attending the event again."),
        automatic=False,
        permission=is_user,
        effects=[
            TransitionEffect('succeed', conditions=[event_is_finished]),
            RelatedTransitionEffect('activity', 'lock', conditions=[event_will_become_full]),
            NotificationEffect(ParticipantApplicationManagerMessage),
            NotificationEffect(ParticipantApplicationMessage),
            FollowActivityEffect
        ]
    )
    reject = Transition(
        ContributionStateMachine.new,
        rejected,
        automatic=False,
        name=_('Reject'),
        description=_("Reject the person if they are not welcome. The person will no longer be attending the event."),
        effects=[
            RelatedTransitionEffect('activity', 'reopen'),
            NotificationEffect(ParticipantRejectedMessage),
            UnFollowActivityEffect
        ],
        permission=is_activity_owner
    )

    accept = Transition(
        rejected,
        ContributionStateMachine.new,
        name=_('Admit'),
        description=_("Admit the person back after previously being rejected. The person will be attending the event again."),
        automatic=False,
        effects=[
            TransitionEffect('succeed', conditions=[event_is_finished]),
            RelatedTransitionEffect('activity', 'lock', conditions=[event_will_become_full]),
            NotificationEffect(ParticipantApplicationMessage),
            FollowActivityEffect
        ],
        permission=is_activity_owner
    )

    mark_absent = Transition(
        ContributionStateMachine.succeeded,
        no_show,
        name=_('Mark absent'),
        description=_("The person didn't show up at the event. Their contribution will no longer be counted."),
        automatic=False,
        permission=is_activity_owner,
        effects=[
            ResetTimeSpent,
            RelatedTransitionEffect(
                'activity', 'expire',
                conditions=[event_is_finished, event_will_be_empty]
            ),
            UnFollowActivityEffect
        ]
    )
    mark_present = Transition(
        no_show,
        ContributionStateMachine.succeeded,
        name=_('Mark present'),
        description=_("The person did show up, after being previously marked absent. Their contribution will be counted."),
        automatic=False,
        permission=is_activity_owner,
        effects=[
            SetTimeSpent,
            RelatedTransitionEffect(
                'activity', 'succeed',
                conditions=[event_is_finished]
            ),
            FollowActivityEffect
        ]
    )

    succeed = Transition(
        ContributionStateMachine.new,
        ContributionStateMachine.succeeded,
        name=_('Succeed'),
        description=_("The person is confirmed at the event. Their contribution will be counted."),
        effects=[
            SetTimeSpent,
            RelatedTransitionEffect(
                'activity', 'succeed',
                conditions=[event_is_finished])
        ]
    )

    reset = Transition(
        ContributionStateMachine.succeeded,
        ContributionStateMachine.new,
        name=_('Reset'),
        description=_("The event is reopened and the person will be joining again. Their contribution will no longer be counted."),
        effects=[ResetTimeSpent]
    )
