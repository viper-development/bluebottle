from django.utils import timezone

from bluebottle.assignments.effects import SetTimeSpent, ClearTimeSpent
from bluebottle.assignments.messages import AssignmentExpiredMessage, AssignmentApplicationMessage, \
    ApplicantAcceptedMessage, ApplicantRejectedMessage, AssignmentCompletedMessage
from bluebottle.follow.effects import UnFollowActivityEffect, FollowActivityEffect
from bluebottle.notifications.effects import NotificationEffect
from django.utils.translation import ugettext_lazy as _

from bluebottle.activities.states import ActivityStateMachine, ContributionStateMachine
from bluebottle.assignments.models import Assignment, Applicant
from bluebottle.fsm.effects import TransitionEffect, RelatedTransitionEffect
from bluebottle.fsm.state import State, Transition, EmptyState


class AssignmentStateMachine(ActivityStateMachine):
    model = Assignment

    running = State(
        _('Running'),
        'running',
        _('The task is taking place and people can’t apply any more.')
    )
    full = State(
        _('Full'),
        'full',
        _('The number of people needed is reached and people can’t apply any more.')
    )
    submitted = State(
        _('Submitted'),
        'submitted',
        _('The task is ready to go online once the initiative has been approved.')
    )

    def should_finish(self):
        """end date has passed"""
        return self.instance.end and self.instance.end < timezone.now()

    def should_start(self):
        """start date has passed"""
        return self.instance.start and self.instance.start < timezone.now() and not self.should_finish()

    def has_deadline(self):
        """has a deadline"""
        return self.instance.end_date_type == 'deadline'

    def is_on_date(self):
        """takes place on a set date"""
        return self.instance.end_date_type == 'on_date'

    def should_open(self):
        """registration deadline is in the future"""
        return self.instance.start and self.instance.start >= timezone.now() and not self.should_finish()

    def has_accepted_applicants(self):
        """there are accepted applicants"""
        return len(self.instance.accepted_applicants) > 0

    def has_no_accepted_applicants(self):
        """there are no accepted applicants"""
        return len(self.instance.accepted_applicants) == 0

    def is_not_full(self):
        """the task is not full"""
        return self.instance.capacity > len(self.instance.accepted_applicants)

    def is_full(self):
        """the task is full"""
        return self.instance.capacity <= len(self.instance.accepted_applicants)

    start = Transition(
        [ActivityStateMachine.open, full],
        running,
        name=_('Start'),
        description=_("Start the task. Triggered when the start time passes."),
        automatic=True,
        effects=[
            RelatedTransitionEffect('accepted_applicants', 'activate'),
        ]
    )

    lock = Transition(
        [ActivityStateMachine.open],
        full,
        automatic=True,
        name=_('Fill'),
        description=_("People can no longer apply. "
                      "Triggered when the number of accepted people equals the number of people needed."),
    )

    approve = Transition(
        [
            ActivityStateMachine.submitted,
            ActivityStateMachine.rejected
        ],
        ActivityStateMachine.open,
        name=_('Approve'),
        automatic=True,
        description=_("The task will be visible in the frontend and people can apply to the task."),
        effects=[
            RelatedTransitionEffect('organizer', 'succeed'),
            TransitionEffect(
                'expire',
                conditions=[should_finish, has_no_accepted_applicants]
            ),
        ]
    )

    cancel = Transition(
        [
            ActivityStateMachine.draft,
            ActivityStateMachine.needs_work,
            ActivityStateMachine.open,
            full,
            running,
            submitted
        ],
        ActivityStateMachine.cancelled,
        name=_('Cancel'),
        description=_('Cancel if the task will not be executed. '
                      'The activity manager will not be able to edit the task and '
                      'it won’t show up on the search page in the front end. '
                      'The task will still be available in the back office and appear in your reporting.'),
        automatic=False,
        effects=[
            RelatedTransitionEffect('organizer', 'fail'),
            RelatedTransitionEffect('accepted_applicants', 'fail')
        ]
    )

    reopen = Transition(
        [
            full,
            ActivityStateMachine.cancelled,
            ActivityStateMachine.succeeded
        ],
        ActivityStateMachine.open,
        name=_('Reopen'),
        description=_("People can apply to the task again. "
                      "Triggered when the number of accepted people become less than the number of people needed."),
        automatic=True
    )

    succeed = Transition(
        [
            ActivityStateMachine.open,
            full,
            running,
            ActivityStateMachine.cancelled
        ],
        ActivityStateMachine.succeeded,
        name=_('Succeed'),
        description=_("The task ends and the contributions are counted. Triggered when the task date passes."),
        automatic=True,
        effects=[
            RelatedTransitionEffect('accepted_applicants', 'succeed'),
            NotificationEffect(AssignmentCompletedMessage)
        ]
    )

    expire = Transition(
        ActivityStateMachine.open,
        ActivityStateMachine.cancelled,
        name=_('Expire'),
        description=_("The task didn’t have any applicants before the deadline to apply and is cancelled."),
        automatic=True,
        effects=[
            RelatedTransitionEffect('organizer', 'fail'),
            NotificationEffect(AssignmentExpiredMessage),
        ]
    )


class ApplicantStateMachine(ContributionStateMachine):
    model = Applicant

    accepted = State(
        _('Accepted'),
        'accepted',
        _('The person was accepted and will participate in the task.')
    )
    rejected = State(
        _('Rejected'),
        'rejected',
        _("The person was rejected and will not participate in the task.")
    )
    withdrawn = State(
        _('Withdrawn'),
        'withdrawn',
        _('The person withdrew and will not participate in the task.')
    )
    no_show = State(
        _('No show'),
        'no_show',
        _('The person did not participate in the task. Their contribution will no longer be counted.')
    )
    active = State(
        _('Active'),
        'active',
        _('The person is currently participating in the task.')
    )

    def has_time_spent(self):
        """time spent is set"""
        return self.instance.time_spent

    def has_no_time_spent(self):
        """time spent is not set"""
        return not self.instance.time_spent

    def is_user(self, user):
        """is applicant"""
        return self.instance.user == user

    def is_activity_owner(self, user):
        """is activity manager or staff member"""
        return user.is_staff or self.instance.activity.owner == user

    def assignment_will_become_full(self):
        """task will be full"""
        activity = self.instance.activity
        return activity.capacity == len(activity.accepted_applicants) + 1

    def assignment_will_become_open(self):
        """task will not be full"""
        activity = self.instance.activity
        return activity.capacity == len(activity.accepted_applicants)

    def assignment_is_finished(self):
        """task is finished"""
        return self.instance.activity.end < timezone.now()

    def assignment_is_not_finished(self):
        "task is not finished"
        return not self.instance.activity.date < timezone.now()

    def assignment_will_be_empty(self):
        """task be empty"""
        return len(self.instance.activity.accepted_applicants) == 1

    def can_accept_applicants(self, user):
        """can accept applicants"""
        return user in [
            self.instance.activity.owner,
            self.instance.activity.initiative.activity_manager,
            self.instance.activity.initiative.owner
        ]

    def assignment_is_open(self):
        """task is open"""
        return self.instance.activity.status == ActivityStateMachine.open.value

    initiate = Transition(
        EmptyState(),
        ContributionStateMachine.new,
        name=_('Apply'),
        description=_("The person wants to participate in the task."),
        effects=[
            NotificationEffect(AssignmentApplicationMessage),
            FollowActivityEffect
        ]
    )

    accept = Transition(
        [
            ContributionStateMachine.new,
            rejected
        ],
        accepted,
        name=_('Accept'),
        description=_("The person will be participating in the task."),
        automatic=False,
        permission=can_accept_applicants,
        effects=[
            TransitionEffect('succeed', conditions=[assignment_is_finished]),
            RelatedTransitionEffect('activity', 'lock', conditions=[assignment_will_become_full]),
            RelatedTransitionEffect(
                'activity',
                'succeed',
                conditions=[assignment_is_finished]
            ),
            NotificationEffect(ApplicantAcceptedMessage)
        ]
    )

    reject = Transition(
        [
            ContributionStateMachine.new,
            accepted
        ],
        rejected,
        name=_('Reject'),
        description=_("The person will not be participating in the task."),
        automatic=False,
        permission=can_accept_applicants,
        effects=[
            RelatedTransitionEffect('activity', 'reopen'),
            NotificationEffect(ApplicantRejectedMessage),
            UnFollowActivityEffect
        ]
    )

    withdraw = Transition(
        [
            ContributionStateMachine.new,
            accepted
        ],
        withdrawn,
        name=_('Withdraw'),
        description=_("The person will voluntarily cease to participate in the task."),
        automatic=False,
        permission=is_user,
        effects=[
            UnFollowActivityEffect
        ]
    )

    reapply = Transition(
        [
            withdrawn,
            ContributionStateMachine.failed
        ],
        ContributionStateMachine.new,
        name=_('Reapply'),
        description=_("The person wants to participate in the task again."),
        automatic=False,
        conditions=[assignment_is_open],
        permission=ContributionStateMachine.is_user,
        effects=[
            FollowActivityEffect
        ]
    )

    activate = Transition(
        [
            accepted,
            # ContributionStateMachine.new
        ],
        active,
        name=_('Start'),
        description=_("The person starts with the task."),
        automatic=True
    )

    succeed = Transition(
        [
            accepted,
            active,
            ContributionStateMachine.new
        ],
        ContributionStateMachine.succeeded,
        name=_('Succeed'),
        description=_("The person has been participating in the task. Their contribution will be counted."),
        automatic=True,
        effects=[
            SetTimeSpent
        ]
    )

    mark_absent = Transition(
        ContributionStateMachine.succeeded,
        no_show,
        name=_('Mark absent'),
        description=_("The person didn't participate in the task. Their contribution will no longer be counted."),
        automatic=False,
        permission=is_activity_owner,
        effects=[
            ClearTimeSpent,
            RelatedTransitionEffect(
                'activity', 'cancel',
                conditions=[assignment_is_finished, assignment_will_be_empty]
            ),
            UnFollowActivityEffect
        ]
    )
    mark_present = Transition(
        no_show,
        ContributionStateMachine.succeeded,
        name=_('Mark present'),
        description=_("The person did participate, after being previously marked absent. "
                      "Their contribution will be counted."),
        automatic=False,
        permission=is_activity_owner,
        effects=[
            SetTimeSpent,
            RelatedTransitionEffect(
                'activity', 'succeed',
                conditions=[assignment_is_finished]
            ),
            FollowActivityEffect
        ]
    )
