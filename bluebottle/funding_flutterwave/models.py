from django.db import models

from bluebottle.fsm import TransitionManager
from bluebottle.funding.models import Payment, PaymentProvider, PaymentMethod, PayoutAccount
from bluebottle.funding.transitions import PaymentTransitions
from django.utils.translation import ugettext_lazy as _


class FlutterwavePayment(Payment):
    tx_ref = models.CharField(max_length=30)
    transitions = TransitionManager(PaymentTransitions, 'status')


class FlutterwavePaymentProvider(PaymentProvider):

    pub_key = models.CharField(max_length=100)
    sec_key = models.CharField(max_length=100)
    prefix = models.CharField(max_length=100, default='goodup')

    currencies = ['NGN']
    countries = ['NG']

    @property
    def payment_methods(self):
        return [
            PaymentMethod(
                provider='flutterwave',
                name='Credit card',
                code='credit_card',
                currencies=['NGN'],
            )
        ]

    @property
    def private_settings(self):
        return {
            'sec_key': self.sec_key
        }

    @property
    def public_settings(self):
        return {
            'pub_key': self.pub_key,
            'prefix': self.prefix
        }


class FlutterwavePayoutAccount(PayoutAccount):

    type = 'flutterwave'
    providers = [
        'flutterwave', 'pledge'
    ]

    account = models.CharField(
        _("flutterwave account"), max_length=100, null=True, blank=True)
    account_holder_name = models.CharField(
        _("account holder name"), max_length=100, null=True, blank=True)
    bank_country_code = models.CharField(
        _("bank country code"), max_length=2, default='NG', null=True, blank=True)
    bank_code = models.CharField(
        _("bank code"), max_length=100, null=True, blank=True)
    account_number = models.CharField(
        _("account number"), max_length=255, null=True, blank=True)
