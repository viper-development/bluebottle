from django.utils.translation import ugettext_lazy as _

from bluebottle.fsm.state import ModelStateMachine, State, EmptyState, AllStates, Transition
from bluebottle.fsm.effects import Effect, TransitionEffect, RelatedTransitionEffect

from bluebottle.activities.models import Organizer, Activity


class CreateOrganizer(Effect):
    "Create an organizer for the event"
    post_save = True

    def execute(self):
        Organizer.objects.get_or_create(activity=self.instance)

    def __unicode__(self):
        return unicode(_('Create organizer'))


class ActivityStateMachine(ModelStateMachine):
    model = Activity

    draft = State(_('draft'), 'draft')
    submitted = State(_('submitted'), 'submitted')
    needs_work = State(_('needs work'), 'needs_work')

    rejected = State(_('rejected'), 'rejected')
    deleted = State(_('deleted'), 'deleted')

    open = State(_('open'), 'open', _('Activity is open, and accepting contributions'))
    succeeded = State(_('succeeded'), 'succeeded', _('The activity is succeeded'))
    closed = State(_('closed'), 'closed')

    def is_complete(self):
        return not list(self.instance.required)

    def is_valid(self):
        return not list(self.instance.errors)

    def initiative_is_approved(self):
        return self.instance.initiative.status == 'approved'

    def initiative_is_not_approved(self):
        return not self.initiative_is_approved()

    def is_staff(self, user):
        return user.is_staff

    def is_owner(self, user):
        return user == self.instance.owner

    initiate = Transition(
        EmptyState(),
        draft,
        name=_('Initiate'),
        effects=[CreateOrganizer]
    )

    submit = Transition(
        draft,
        submitted,
        name=_('Submit'),
        effects=[
            TransitionEffect('approve', conditions=[initiative_is_approved])
        ]
    )

    approve = Transition(
        [draft, submitted, rejected],
        open,
        automatic=False,
        permission=is_staff,
        name=_('Approve'),
        effects=[
            RelatedTransitionEffect('organizer', 'succeed')
        ]
    )

    reject = Transition(
        AllStates(),
        rejected,
        name=_('Reject'),
        automatic=False,
        permission=is_staff,
        effects=[RelatedTransitionEffect('organizer', 'fail')]
    )
    accept = Transition(
        rejected,
        draft,
        name=_('Accept'),
        automatic=False,
        permission=is_staff,
        effects=[RelatedTransitionEffect('organizer', 'reset')]
    )

    delete = Transition(
        [draft, needs_work, submitted],
        deleted,
        name=_('Delete'),
        automatic=False,
        permissions=is_owner,
        effects=[RelatedTransitionEffect('organizer', 'fail')]
    )


class ContributionStateMachine(ModelStateMachine):
    new = State(_('new'), 'new')
    succeeded = State(_('succeeded'), 'succeeded')
    failed = State(_('failed'), 'failed')
    closed = State(_('closed'), 'closed')

    initiate = Transition(EmptyState(), new)
    close = Transition(
        (new, succeeded, failed, ),
        closed
    )


class OrganizerStateMachine(ContributionStateMachine):
    model = Organizer

    succeed = Transition(
        (ContributionStateMachine.new, ContributionStateMachine.failed, ),
        ContributionStateMachine.succeeded
    )
    fail = Transition(
        AllStates(),
        ContributionStateMachine.failed
    )
    reset = Transition(
        (ContributionStateMachine.succeeded, ContributionStateMachine.closed, ),
        ContributionStateMachine.new,
    )