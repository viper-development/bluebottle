from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from bluebottle.activities.states import ActivityStateMachine, ContributionStateMachine
from bluebottle.follow.effects import FollowActivityEffect
from bluebottle.fsm.effects import (
    TransitionEffect,
    RelatedTransitionEffect
)
from bluebottle.fsm.state import Transition, ModelStateMachine, State
from bluebottle.funding.effects import GeneratePayouts, GenerateDonationWallpost, \
    RemoveDonationWallpost, UpdateFundingAmounts, RefundPaymentAtPSP
from bluebottle.funding.messages import DonationSuccessActivityManagerMessage, DonationSuccessDonorMessage
from bluebottle.funding.models import Funding, Donation, Payout, Payment
from bluebottle.notifications.effects import NotificationEffect


class FundingStateMachine(ActivityStateMachine):

    model = Funding

    partially_funded = State(_('partially funded'), 'partially_funded')
    refunded = State(_('refunded'), 'refunded')

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

    succeed = Transition(
        [ActivityStateMachine.open, partially_funded],
        ActivityStateMachine.succeeded,
        name=_('Succeed'),
        automatic=True,
        effects=[
            GeneratePayouts
        ]
    )

    recalculate = Transition(
        ActivityStateMachine.succeeded,
        ActivityStateMachine.succeeded,
        name=_('Recalculate'),
        automatic=False,
        effects=[
            GeneratePayouts
        ]
    )

    partial = Transition(
        [ActivityStateMachine.open, ActivityStateMachine.succeeded],
        partially_funded,
        name=_('Partial'),
        automatic=True,
        effects=[
            GeneratePayouts
        ]
    )

    refund = Transition(
        [ActivityStateMachine.succeeded, partially_funded],
        refunded,
        name=_('Refund'),
        automatic=False,
        effects=[
            RelatedTransitionEffect('donations', 'activity_refund'),
            RelatedTransitionEffect('payouts', 'cancel')
        ]
    )


class DonationStateMachine(ContributionStateMachine):
    model = Donation
    failed = State(_('failed'), 'failed')
    refunded = State(_('refunded'), 'refunded')
    activity_refunded = State(_('activity_refunded'), 'activity_refunded')

    succeed = Transition(
        [
            ContributionStateMachine.new,
            ContributionStateMachine.failed
        ],
        ContributionStateMachine.succeeded,
        name=_('Succeed'),
        automatic=True,
        effects=[
            NotificationEffect(DonationSuccessActivityManagerMessage),
            NotificationEffect(DonationSuccessDonorMessage),
            GenerateDonationWallpost,
            FollowActivityEffect,
            UpdateFundingAmounts
        ]
    )

    fail = Transition(
        [
            ContributionStateMachine.new,
            ContributionStateMachine.succeeded
        ],
        failed,
        name=_('Fail'),
        automatic=True,
        effects=[
            RemoveDonationWallpost,
            UpdateFundingAmounts
        ]
    )

    refund = Transition(
        [
            ContributionStateMachine.new,
            ContributionStateMachine.succeeded
        ],
        refunded,
        name=_('Refund'),
        automatic=True,
        effects=[
            RelatedTransitionEffect('payment', 'refund'),
            RemoveDonationWallpost,
            UpdateFundingAmounts
        ]
    )

    activity_refund = Transition(
        [
            ContributionStateMachine.new,
            ContributionStateMachine.succeeded,
        ],
        activity_refunded,
        name=_('Activity refund'),
        automatic=True,
        effects=[
            RelatedTransitionEffect('payment', 'refund'),
            RemoveDonationWallpost
        ]
    )


class PaymentStateMachine(ModelStateMachine):
    model = Payment

    new = State(_('new'), 'new')
    pending = State(_('pending'), 'pending')
    succeeded = State(_('succeeded'), 'succeeded')
    failed = State(_('failed'), 'failed')
    refunded = State(_('refunded'), 'refunded')
    activity_refunded = State(_('activity_refunded'), 'activity_refunded')

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

    refund = Transition(
        [
            ContributionStateMachine.succeeded
        ],
        refunded,
        name=_('Refund'),
        automatic=True,
        effects=[
            RefundPaymentAtPSP
        ]
    )

    activity_refund = Transition(
        [
            ContributionStateMachine.succeeded
        ],
        activity_refunded,
        name=_('Activity refund'),
        automatic=True,
        effects=[
            RemoveDonationWallpost
        ]
    )


class PayoutStateMachine(ModelStateMachine):
    model = Payout

    new = State(_('new'), 'new')
    approved = State(_('approve'), 'approve')
    scheduled = State(_('scheduled'), 'scheduled')
    started = State(_('started'), 'started')
    succeeded = State(_('succeeded'), 'succeeded')
    failed = State(_('failed'), 'failed')

    approve = Transition(
        new,
        approved,
        name=_('Approve'),
        automatic=False
    )

    start = Transition(
        new,
        started,
        name=_('Start'),
        automatic=True
    )

    reset = Transition(
        [approved, scheduled, started, succeeded, failed],
        new,
        name=_('Reset'),
        automatic=True
    )

    succeed = Transition(
        [approved, scheduled, started, failed],
        succeeded,
        name=_('Succeed'),
        automatic=True
    )

    cancel = Transition(
        [new, approved],
        failed,
        name=_('Cancel'),
        automatic=True
    )
