from rest_framework import authentication, exceptions

from bluebottle.activity_pub.models import Server
from bluebottle.activity_pub.utils import verify_request_signature


class ServerSignatureAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        server = None
        public_key = None

        try:
            server = Server.from_request(request)
            public_key = server.public_key
        except Server.DoesNotExist:
            if request.method == 'POST':
                try:
                    public_key = request.data['public_key']
                except KeyError:
                    raise exceptions.AuthenticationFailed(
                        'No pubic key found in request'
                    )
            else:
                raise exceptions.AuthenticationFailed(
                    'No matching server found'
                )

        if not verify_request_signature(request, public_key):
            raise exceptions.AuthenticationFailed(
                'Invalid signature'
            )

        return (server, public_key)
