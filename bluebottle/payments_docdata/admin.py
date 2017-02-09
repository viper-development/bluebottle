from django.contrib import admin
from bluebottle.payments_logger.admin import PaymentLogEntryInline
from django.core.urlresolvers import reverse
from django.utils.html import format_html

from polymorphic.admin import PolymorphicChildModelAdmin

from bluebottle.payments.models import Payment
from bluebottle.payments_docdata.models import (
    DocdataPayment, DocdataDirectdebitPayment, DocdataTransaction)


class DocdataTransactionInline(admin.TabularInline):
    model = DocdataTransaction
    readonly_fields = ('status', 'created', 'updated', 'docdata_id',
                       'payment_method', 'authorization_status',
                       'authorization_amount')
    fields = readonly_fields
    can_delete = False

    def has_add_permission(self, request):
        return False

    class Media:
        css = {"all": ("css/admin/hide_admin_original.css",)}


class AbstractDocdataPaymentAdmin(PolymorphicChildModelAdmin):
    base_model = Payment
    inlines = (PaymentLogEntryInline, DocdataTransactionInline)

    readonly_fields = (
        'order_payment_link', 'merchant_order_id', 'payment_cluster_link',
        'payment_cluster_key', 'ideal_issuer_id', 'default_pm',
        'total_gross_amount',
        'currency')

    def order_payment_link(self, obj):
        object = obj.order_payment
        url = reverse('admin:{0}_{1}_change'.format(object._meta.app_label,
                                                    object._meta.model_name),
                      args=[object.id])
        return format_html(
            u"<a href='{}'>Order Payment: {}</a>",
            str(url),
            object.id
        )

    def payment_cluster_link(self, obj):
        url = ('https://backoffice.docdatapayments.com/ps/com.tripledeal.'
               'paymentservice.backoffice.MerchantReportPayoutTransaction')
        return format_html(
            u'{} <a href="{}" target="docdata">[Docdata Backoffice]</a>',
            obj.payment_cluster_id, url
        )


class DocdataPaymentAdmin(AbstractDocdataPaymentAdmin):
    model = DocdataPayment

    readonly_fields = AbstractDocdataPaymentAdmin.readonly_fields + (
        'ip_address', 'customer_id', 'email', 'first_name', 'last_name',
        'address', 'postal_code', 'city', 'country',
    )

    fields = ('status',) + readonly_fields


class DocdataDirectdebitPaymentAdmin(AbstractDocdataPaymentAdmin):
    model = DocdataDirectdebitPayment

    readonly_fields = AbstractDocdataPaymentAdmin.readonly_fields + (
        'total_registered', 'total_shopper_pending', 'total_acquirer_pending',
        'total_acquirer_approved', 'total_captured', 'total_refunded',
        'total_charged_back', 'iban', 'bic', 'agree', 'account_name',
        'account_city')

    fields = readonly_fields
