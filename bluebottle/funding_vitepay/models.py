from django.db import models
from django.utils.translation import ugettext_lazy as _
from djchoices import DjangoChoices, ChoiceItem

from bluebottle.funding.models import Payment, PaymentProvider


class VitepayPayment(Payment):
    intent_id = models.CharField(max_length=30)
    client_secret = models.CharField(max_length=100)

    @property
    def unique_id(self):
        return "Payment-{}".format(self.id)


class VitepayPaymentProvider(PaymentProvider):

    provider = 'Vitepay'

    class Methods(DjangoChoices):
        orange_money = ChoiceItem('orange_money', label=_('Orange money'))

    default_method = Methods.orange_money

    api_secret = models.CharField(max_length=100)
    api_key = models.CharField(max_length=100)
    api_url = models.CharField(max_length=100, default='https://api.vitepay.com/v1/prod/payments')

    @property
    def private_settings(self):
        return {
            'api_secret': self.api_secret,
            'api_key': self.api_key,
            'api_url': self.api_url
        }
