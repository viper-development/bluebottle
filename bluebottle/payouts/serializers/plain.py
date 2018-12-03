from rest_framework import serializers

from bluebottle.bluebottle_drf2.serializers import PrivateFileSerializer
from bluebottle.payouts.models.plain import PlainPayoutAccount, PayoutDocument
from bluebottle.utils.permissions import ResourceOwnerPermission


class PayoutDocumentSerializer(serializers.ModelSerializer):

    file = PrivateFileSerializer(
        'payout-document-file', url_args=('pk', ), permission=ResourceOwnerPermission
    )

    class Meta:
        model = PayoutDocument
        fields = ('id', 'file')


class PlainPayoutAccountSerializer(serializers.ModelSerializer):

    document = PayoutDocumentSerializer(required=False)

    class Meta:
        model = PlainPayoutAccount
        fields = (
            'id',
            'account_holder_name',
            'account_holder_address',
            'account_holder_postal_code',
            'account_holder_city',
            'account_holder_country',
            'account_number',
            'account_details',
            'account_bank_country',
            'document'
        )
