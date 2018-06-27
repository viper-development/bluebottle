from decimal import Decimal

from django.db import models
from django.utils.translation import ugettext_lazy as _

from bluebottle.payments.models import Payment
from bluebottle.projects.models import ProjectAddOn


class CellulantPayment(Payment):

    reference = models.CharField(
        help_text="Transaction reference",
        null=True, blank=True,
        max_length=200)

    msisdn = models.CharField(
        help_text="Cellulant msisdn (phone number)",
        null=True, blank=True,
        max_length=200)

    account_number = models.CharField(
        help_text="Cellulant account number",
        null=True, blank=True,
        max_length=200)

    amount = models.CharField(
        help_text="Cellulant amount",
        null=True, blank=True,
        max_length=200)

    currency = models.CharField(
        help_text="Cellulant currency code",
        null=True, blank=True,
        max_length=200)

    country_code = models.CharField(
        help_text="Cellulant country code",
        null=True, blank=True,
        max_length=200)

    payment_method = models.CharField(
        help_text="Cellulant payment method",
        null=True, blank=True,
        max_length=200)

    language = models.CharField(
        help_text="Cellulant language code",
        null=True, blank=True,
        max_length=200)

    payment_option = models.CharField(
        help_text="Cellulant payment option",
        null=True, blank=True,
        max_length=200)

    payment_mode = models.CharField(
        help_text="Cellulant payment mode",
        null=True, blank=True,
        max_length=200)

    callback_url = models.CharField(
        help_text="Cellulant callback url",
        null=True, blank=True,
        max_length=200)

    response = models.TextField(help_text=_('Response from Cellulant'), null=True, blank=True)
    update_response = models.TextField(help_text=_('Result from Cellulant (status update)'), null=True, blank=True)

    class Meta:
        ordering = ('-created', '-updated')
        verbose_name = "Cellulant Payment"
        verbose_name_plural = "Cellulant Payments"

    def get_method_name(self):
        """ Return the payment method name."""
        return 'cellulant'

    def get_fee(self):
        """
        a fee of 1.5% of the value of the transaction.
        """
        fee = round(self.order_payment.amount * Decimal(0.015), 2)
        return fee


class CellulantProject(ProjectAddOn):

    type = 'mpesa'
    serializer = 'bluebottle.payments_cellulant.serializers.BaseProjectAddOnSerializer'
    account_number = models.CharField(max_length=100, null=True, blank=True,
                                      help_text='Cellulant account number')

    @property
    def paybill_number(self):
        from bluebottle.payments_cellulant.adapters import CellulantPaymentInterface
        return CellulantPaymentInterface().credentials['business_number']

    def __unicode__(self):
        return "{} - {}".format(self.account_number, self.project.title)
