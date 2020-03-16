import json
import httpsig

from django.urls import reverse
from django.utils import timezone

from bluebottle.test.utils import BluebottleTestCase

from bluebottle.clients.models import Client
from bluebottle.clients.utils import LocalTenant
from bluebottle.test.utils import JSONAPITestClient
from bluebottle.activity_pub.models import ActivityPubPlatformSettings


class SignedRequestClient(JSONAPITestClient):
    def generic(self, method, path, *args, **extra):
        if 'private_key' in extra:
            extra['HTTP_DATE'] = timezone.now().isoformat()
            signer = httpsig.HeaderSigner(
                self.tenant.domain_url,
                extra['private_key'],
                algorithm="rsa-sha256",
                headers=['(request-target)', 'host', 'date']
            )
            signed_headers_dict = signer.sign(
                {
                    'Date': extra['HTTP_DATE'],
                    'Host': self.tenant.domain_url
                },
                method=method,
                path=path
            )
            extra['HTTP_AUTHORIZATION'] = signed_headers_dict['authorization']

        return super(SignedRequestClient, self).generic(
            method, path, *args, **extra
        )


class ExchangeKeysTestCase(BluebottleTestCase):
    def setUp(self):
        super(ExchangeKeysTestCase, self).setUp()
        self.remote = Client.objects.get(client_name='test2')

        self.remote_client = SignedRequestClient(self.remote)

        with LocalTenant(self.remote):
            self.remote.domain_url = self.remote.domain_url + '.org'
            self.remote.save()

        self.tenant.domain_url = self.tenant.domain_url + '.org'
        self.tenant.save()

        (self.pub_settings, _created) = ActivityPubPlatformSettings.objects.get_or_create()

    def test_request(self):

        data = {
            'data': {
                'type': 'servers',
                'attributes': {
                    'name': self.tenant.name,
                    'domain': 'http://{}'.format(self.tenant.domain_url),
                    'public_key': self.pub_settings.public_key,
                    'logo': 'http://{}/images/logo.svg'.format(self.tenant.domain_url)
                }
            }
        }

        response = self.remote_client.post(
            reverse('related-platform-view'),
            data=json.dumps(data),
            private_key=self.pub_settings.secret_key
        )

        self.assertTrue(response.status_code, 200)
