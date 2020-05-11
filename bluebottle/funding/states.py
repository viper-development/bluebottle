from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from bluebottle.activities.states import ActivityStateMachine, ContributionStateMachine

from bluebottle.fsm.effects import (
    TransitionEffect,
    RelatedTransitionEffect
)
from bluebottle.fsm.state import Transition, ModelStateMachine, State
from bluebottle.funding.models import Funding, Donation, Payout, Payment


class FundingStateMachine(ActivityStateMachine):

    model = Funding

    def should_finish(self):
        """the deadline has passed"""
        return self.instance.deadline and self.instance.deadline < timezone.now()

    def deadline_in_future(self):
        if not self.instance.deadline >= timezone.now():
            return _("The deadline of the activity should be in the future.")

    def target_reached(self):
        return self.instance.amount_raised >= self.instance.target

    def target_not_reached(self):
        return not self.target_reached

    submit = Transition(
        [
            ActivityStateMachine.draft,
            ActivityStateMachine.needs_work
        ],
        ActivityStateMachine.submitted,
        name=_('Submit'),
        conditions=[
            ActivityStateMachine.is_complete,
            ActivityStateMachine.is_valid
        ],
        automatic=False
    )

    approve = Transition(
        [
            ActivityStateMachine.draft,
            ActivityStateMachine.needs_work,
            ActivityStateMachine.submitted,
            ActivityStateMachine.rejected
        ],
        ActivityStateMachine.open,
        name=_('Approve'),
        automatic=False,
        effects=[
            RelatedTransitionEffect('organizer', 'succeed'),
            TransitionEffect(
                'close',
                conditions=[should_finish]
            ),
        ]
    )


class DonationStateMachine(ContributionStateMachine):
    model = Donation
    failed = State(_('failed'), 'failed')

    fail = Transition(
        [
            ContributionStateMachine.new,
            ContributionStateMachine.succeeded
        ],
        failed,
        name=_('Fail'),
        automatic=True
    )


class PaymentStateMachine(ModelStateMachine):
    model = Payment

    new = State(_('new'), 'new')
    pending = State(_('pending'), 'pending')
    succeeded = State(_('succeeded'), 'succeeded')
    failed = State(_('failed'), 'failed')

    succeed = Transition(
        [new, pending, failed],
        succeeded,
        name=_('Succeed'),
        automatic=True
    )

    fail = Transition(
        [new, pending, succeeded],
        failed,
        name=_('Fail'),
        automatic=True
    )


class PayoutStateMachine(ModelStateMachine):
    model = Payout

    new = State(_('new'), 'new')
    pending = State(_('pending'), 'pending')
    succeeded = State(_('succeeded'), 'succeeded')
    failed = State(_('failed'), 'failed')
