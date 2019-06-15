from django.conf import settings
from django.db import models, connection
from django.utils.translation import ugettext_lazy as _
from djchoices import DjangoChoices, ChoiceItem

from bluebottle.funding.models import Payment, PaymentProvider
from bluebottle.funding_stripe.utils import StripeMixin
from bluebottle.payouts.models import StripePayoutAccount


class StripePayment(Payment, StripeMixin):
    intent_id = models.CharField(max_length=30)
    client_secret = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.pk:
            intent = self.stripe.PaymentIntent.create(
                amount=int(self.donation.amount.amount * 100),
                currency=self.donation.amount.currency,
                transfer_data={
                    'destination': StripePayoutAccount.objects.all()[0].account_id,
                },
                metadata=self.metadata
            )
            self.intent_id = intent.id
            self.client_secret = intent.client_secret

        super(StripePayment, self).save(*args, **kwargs)

    def update(self):
        intent = self.stripe.PaymentIntent.retrieve(self.intent_id)
        if len(intent.charges) == 0:
            # No charge. Do we still need to charge?
            self.fail()
            self.save()
        elif intent.charges.data[0].refunded and self.status != Payment.Status.refunded:
            self.refund()
            self.save()
        elif intent.status == 'failed' and self.status != Payment.Status.failed:
            self.fail()
            self.save()
        elif intent.status == 'succeeded' and self.status != Payment.Status.success:
            self.succeed()
            self.save()

    @property
    def metadata(self):
        return {
            "tenant_name": connection.tenant.client_name,
            "tenant_domain": connection.tenant.domain_url,
            "activity_id": self.donation.activity.pk,
            "activity_title": self.donation.activity.title,
        }

    @Payment.status.transition(
        source=['success'],
        target='refunded'
    )
    def request_refund(self):
        intent = self.stripe.PaymentIntent.retrieve(self.intent_id)

        intent.charges[0].refund(
            reverse_transfer=True,
        )


class StripePaymentProvider(PaymentProvider):

    provider = 'Stripe'

    class Methods(DjangoChoices):
        credit_card = ChoiceItem('credit_card', label=_('Credit card'))
        direct_debit = ChoiceItem('direct_debit', label=_('Direct debit'))
        ideal = ChoiceItem('ideal', label=_('iDEAL'))
        bancontact = ChoiceItem('bancontact', label=_('Bancontact'))

    default_method = Methods.credit_card

    @property
    def public_settings(self):
        return settings.STRIPE['public']

    @property
    def private_settings(self):
        return settings.STRIPE['private']
