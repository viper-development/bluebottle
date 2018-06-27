from polymorphic.admin import PolymorphicChildModelAdmin

from django.contrib import admin
from bluebottle.payments.models import Payment
from bluebottle.payments_cellulant.models import CellulantProject

from .models import CellulantPayment


class CellulantPaymentAdmin(PolymorphicChildModelAdmin):
    base_model = Payment
    model = CellulantPayment
    search_fields = ['msisdn', 'transaction_reference']
    raw_id_fields = ('order_payment', )


admin.site.register(CellulantPayment, CellulantPaymentAdmin)


class CellulantProjectAdmin(admin.ModelAdmin):
    raw_id_fields = ('project', )


admin.site.register(CellulantProject, CellulantProjectAdmin)
