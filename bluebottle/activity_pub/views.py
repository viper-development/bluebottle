from bluebottle.utils.views import (
    CreateAPIView, JsonApiViewMixin
)

from bluebottle.activity_pub.models import Server
from bluebottle.activity_pub.authentication import ServerSignatureAuthentication
from bluebottle.activity_pub.serializers import ServerSerializer


class RelatedPlatformView(JsonApiViewMixin, CreateAPIView):
    permission_classes = []
    authentication_classes = [ServerSignatureAuthentication]

    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    model = Server
