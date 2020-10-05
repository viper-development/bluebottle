from bluebottle.funding.effects import SubmitConnectedActivitiesEffect
from django.utils.translation import ugettext_lazy as _

from bluebottle.fsm.effects import RelatedTransitionEffect
from bluebottle.fsm.state import Transition, State
from bluebottle.funding.states import BasePaymentStateMachine, PayoutAccountStateMachine, BankAccountStateMachine
from bluebottle.funding_stripe.models import StripePayment, StripeSourcePayment, StripePayoutAccount, ExternalAccount


class StripePaymentStateMachine(BasePaymentStateMachine):
    model = StripePayment


class StripeSourcePaymentStateMachine(BasePaymentStateMachine):

    model = StripeSourcePayment

    charged = State(_('charged'), 'charged')
    canceled = State(_('canceled'), 'canceled')
    disputed = State(_('disputed'), 'disputed')

    def has_charge_token(self):
        return bool(self.instance.charge_token)

    def is_not_refunded(self):
        return self.instance.status not in ['refunded', 'disputed']

    authorize = Transition(
        [
            BasePaymentStateMachine.new,
            charged
        ],
        BasePaymentStateMachine.pending,
        name=_('Authorize'),
        automatic=True,
        effects=[
            RelatedTransitionEffect('donation', 'succeed')
        ]
    )

    succeed = Transition(
        [
            BasePaymentStateMachine.new,
            BasePaymentStateMachine.pending,
            charged
        ],
        BasePaymentStateMachine.succeeded,
        name=_('Succeed'),
        automatic=True,
        effects=[
            RelatedTransitionEffect('donation', 'succeed')
        ]
    )

    charge = Transition(
        BasePaymentStateMachine.new,
        charged,
        name=_('Charge'),
        automatic=True,
        conditions=[has_charge_token]
    )

    cancel = Transition(
        BasePaymentStateMachine.new,
        canceled,
        name=_('Canceled'),
        automatic=True,
        effects=[
            RelatedTransitionEffect('donation', 'fail')
        ]
    )

    dispute = Transition(
        [
            BasePaymentStateMachine.new,
            BasePaymentStateMachine.succeeded,
        ],
        disputed,
        name=_('Dispute'),
        automatic=True,
        effects=[
            RelatedTransitionEffect('donation', 'refund')
        ]
    )


class StripePayoutAccountStateMachine(PayoutAccountStateMachine):
    model = StripePayoutAccount


class StripeBankAccountStateMachine(BankAccountStateMachine):
    model = ExternalAccount

    reject = Transition(
        [
            BankAccountStateMachine.verified,
            BankAccountStateMachine.unverified,
            BankAccountStateMachine.incomplete],
        BankAccountStateMachine.rejected,
        name=_('Reject'),
        description=_("Reject bank account"),
        automatic=True,
        effects=[
            SubmitConnectedActivitiesEffect
        ]
    )

    verify = Transition(
        [
            BankAccountStateMachine.incomplete,
            BankAccountStateMachine.unverified
        ],
        BankAccountStateMachine.verified,
        name=_('Verify'),
        description=_("Verify that the bank account is complete."),
        automatic=True
    )
