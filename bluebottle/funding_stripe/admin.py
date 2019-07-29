from django.contrib import admin

from bluebottle.funding.admin import PaymentChildAdmin, PaymentProviderChildAdmin, PayoutAccountAdmin
from bluebottle.funding_stripe.models import StripePayment, StripePaymentProvider, StripePayoutAccount


@admin.register(StripePayment)
class StripePaymentAdmin(PaymentChildAdmin):
    base_model = StripePayment


@admin.register(StripePaymentProvider)
class PledgePaymentProviderAdmin(PaymentProviderChildAdmin):
    base_model = StripePaymentProvider


@admin.register(StripePayoutAccount)
class StripePayoutAccountAdmin(PayoutAccountAdmin):
    model = StripePayoutAccount
