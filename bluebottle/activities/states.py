from django.utils.translation import ugettext_lazy as _

from bluebottle.activities.models import Organizer
from bluebottle.fsm.effects import Effect, TransitionEffect, RelatedTransitionEffect
from bluebottle.fsm.state import ModelStateMachine, State, EmptyState, AllStates, Transition


class CreateOrganizer(Effect):
    "Create an organizer for the activity"
    post_save = True

    def execute(self, **kwargs):
        Organizer.objects.get_or_create(
            activity=self.instance,
            defaults={'user': self.instance.owner}
        )

    def __unicode__(self):
        return unicode(_('Create organizer'))


class ActivityStateMachine(ModelStateMachine):
    draft = State(
        _('Draft'),
        'draft',
        _('The activity has been created, but not yet completed. The activity manager is still editing the activity.')
    )
    submitted = State(
        _('Submitted'),
        'submitted',
        _('The activity is ready to go online once the initiative has been approved.')
    )
    needs_work = State(
        _('Needs work'),
        'needs_work',
        _('The activity has been submitted but needs adjustments in order to be approved.')
    )
    rejected = State(
        _('Rejected'),
        'rejected',
        _('The activity doesn’t fit the program or the rules of the game. '
          'The activity won’t show up on the search page in the front end, '
          'but does count in the reporting. '
          'The activity cannot be edited by the activity manager.')
    )
    deleted = State(
        _('Deleted'),
        'deleted',
        _('The activity is not visible in the frontend and does not count in the reporting. '
          'The activity cannot be edited by the activity manager.')
    )
    cancelled = State(
        _('Cancelled'),
        'cancelled',
        _('The activity is not executed. '
          'The activity won’t show up on the search page in the front end, '
          'but does count in the reporting. '
          'The activity cannot be edited by the activity manager.')
    )
    open = State(
        _('Open'),
        'open',
        _('The activity is accepting new contributions.')
    )
    succeeded = State(
        _('Succeeded'),
        'succeeded',
        _('The activity has ended successfully.')
    )

    def is_complete(self):
        """all required information has been submitted"""
        return not list(self.instance.required)

    def is_valid(self):
        """all fields passed validation and are correct"""
        return not list(self.instance.errors)

    def initiative_is_approved(self):
        """the initiative has been approved"""
        return self.instance.initiative.status == 'approved'

    def initiative_is_submitted(self):
        """the initiative has been submitted"""
        return self.instance.initiative.status in ('submitted', 'approved')

    def initiative_is_not_approved(self):
        """the initiative has not yet been approved"""
        return not self.initiative_is_approved()

    def is_staff(self, user):
        """user is a staff member"""
        return user.is_staff

    def is_owner(self, user):
        """user is the owner"""
        return user == self.instance.owner

    initiate = Transition(
        EmptyState(),
        draft,
        name=_('Initiate'),
        effects=[CreateOrganizer]
    )

    submit = Transition(
        [
            draft,
            needs_work,
            cancelled
        ],
        submitted,
        description=_('The activity will be submitted for review.'),
        automatic=False,
        name=_('Submit'),
        conditions=[is_complete, is_valid, initiative_is_submitted],
        effects=[
            TransitionEffect('approve', conditions=[initiative_is_approved])
        ]
    )

    approve = Transition(
        [
            submitted,
            rejected,
            needs_work
        ],
        open,
        automatic=False,
        permission=is_staff,
        name=_('Approve'),
        effects=[
            RelatedTransitionEffect('organizer', 'succeed')
        ]
    )

    reject = Transition(
        [
            draft,
            needs_work,
            submitted
        ],
        rejected,
        name=_('Reject'),
        description=_('Reject in case this activity doesn’t fit your program or the rules of the game. '
                      'The activity owner will not be able to edit the activity and it won’t show up on '
                      'the search page in the front end. The activity will still be available in the '
                      'back office and appear in your reporting.'),
        automatic=False,
        permission=is_staff,
        effects=[
            RelatedTransitionEffect('organizer', 'fail')
        ]
    )

    cancel = Transition(
        [
            draft,
            needs_work,
            submitted
        ],
        cancelled,
        name=_('Cancel'),
        description=_('Cancel if the activity will not be executed. '
                      'The activity manager will not be able to edit '
                      'the activity and it won’t show up on the search page in the front end. '
                      'The activity will still be available in the back office and appear in your reporting.'),
        automatic=False,
        effects=[
            RelatedTransitionEffect('organizer', 'fail')
        ]
    )

    restore = Transition(
        [
            rejected,
            cancelled,
            deleted
        ],
        draft,
        name=_('Restore'),
        description=_('The status of the activity is set to "Draft". The activity owner can edit the activity again.'),
        automatic=False,
        permission=is_staff,
        effects=[
            RelatedTransitionEffect('organizer', 'reset')
        ]
    )

    delete = Transition(
        [draft, needs_work, submitted, cancelled, rejected],
        deleted,
        name=_('Delete'),
        automatic=False,
        permission=is_owner,
        description=_('Delete the activity if you don’t want it to appear in your reporting. '
                      'The activity will still be available in the back office.'),
        effects=[
            RelatedTransitionEffect('organizer', 'fail')
        ]
    )

    succeed = Transition(
        open,
        succeeded,
        name=_('Succeed'),
        automatic=True,
    )


class ContributionStateMachine(ModelStateMachine):
    new = State(
        _('New'),
        'new',
        _("The user started a contribution")
    )
    succeeded = State(
        _('Succeeded'),
        'succeeded',
        _("The contribution was successful.")
    )
    failed = State(
        _('Failed'),
        'failed',
        _("The contribution failed.")
    )

    def is_user(self, user):
        return self.instance.user == user

    initiate = Transition(
        EmptyState(),
        new,
        name=_('Initiate'),
        description=_('The contribution was created.')
    )
    fail = Transition(
        (new, succeeded, failed, ),
        failed,
        name=_('Fail'),
        description=_("The contribution failed. It will not be visible in reports."),
    )


class OrganizerStateMachine(ContributionStateMachine):
    model = Organizer

    succeed = Transition(
        [
            ContributionStateMachine.new,
            ContributionStateMachine.failed
        ],
        ContributionStateMachine.succeeded,
        name=_('Succeed'),
        description=_('The organizer was successful in setting up the activity.')
    )
    fail = Transition(
        AllStates(),
        ContributionStateMachine.failed,
        name=_('Fail'),
        description=_('The organizer failed to set up the activity.')
    )
    reset = Transition(
        [
            ContributionStateMachine.succeeded,
            ContributionStateMachine.failed
        ],
        ContributionStateMachine.new,
        name=_('Reset'),
        description=_('The organizer is still busy setting up the activity.')
    )
