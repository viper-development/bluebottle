from rest_framework import serializers

from bluebottle.utils.model_dispatcher import get_organization_model, get_organizationmember_model
from bluebottle.utils.serializers import URLField

ORGANIZATION_MODEL = get_organization_model()
MEMBER_MODEL = get_organizationmember_model()


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ORGANIZATION_MODEL
        fields = ('id', 'name', 'slug', 'address_line1', 'address_line2',
                  'city', 'state', 'country', 'postal_code', 'phone_number',
                  'website', 'email')


class ManageOrganizationSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False)
    name = serializers.CharField(required=True)
    website = URLField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = ORGANIZATION_MODEL
        fields = OrganizationSerializer.Meta.field + ('partner_organizations',
                                                      'created', 'updated')
