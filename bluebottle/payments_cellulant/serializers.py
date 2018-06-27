from rest_framework import serializers

from bluebottle.payments_cellulant.models import CellulantProject


class BaseProjectAddOnSerializer(serializers.ModelSerializer):

    paybill_number = serializers.CharField()

    class Meta:
        model = CellulantProject
        fields = ('id', 'type', 'account_number', 'paybill_number')
