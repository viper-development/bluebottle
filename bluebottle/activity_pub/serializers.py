from rest_framework import serializers, exceptions
from rest_framework_json_api.serializers import ModelSerializer

from bluebottle.activity_pub.models import Server


class ServerSerializer(ModelSerializer):
    local_properties = serializers.SerializerMethodField()

    def get_local_properties(self, obj):
        return Server.local_properties

    class Meta:
        model = Server
        fields = ('id', 'domain', 'name', 'logo', 'public_key', 'local_properties', )

    class JSONAPIMeta:
        resource_name = 'servers'

    def perform_create(self, serializer):
        if not serializer.instance.verifiy_signature(self.request):
            raise exceptions.AuthenticationFailed(
                'Invalid signature'
            )

        super(ServerSerializer, self).save()
