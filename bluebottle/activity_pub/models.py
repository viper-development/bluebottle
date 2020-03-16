
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

import httpsig

from django.db import models, connection
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import classproperty

from bluebottle.utils.models import BasePlatformSettings


class Server(models.Model):
    name = models.CharField(max_length=100)
    domain = models.URLField(max_length=100)
    logo = models.URLField(max_length=100)
    location = models.URLField(max_length=100)

    public_key = models.TextField(blank=True, null=True)

    accepted = models.BooleanField(default=False)
    server_accepted = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Server")
        verbose_name_plural = _("Servers")

    @classmethod
    def create(cls, domain):
        pass

    @classmethod
    def from_request(cls, request):
        auth_dict = httpsig.utils.parse_signature_header(
            request.META['HTTP_AUTHORIZATION']
        )

        return cls.objects.get(domain=auth_dict['keyid'])

    @classproperty
    def local_properties(cls):
        settings = ActivityPubPlatformSettings.objects.get()

        return {
            'name': connection.tenant.name,
            'domain': 'http://{}'.format(connection.tenant.domain_url),
            'public_key': settings.public_key,
            'logo': 'http://{}/images/logo.svg'.format(connection.tenant.domain_url)
        }


class ActivityPubPlatformSettings(BasePlatformSettings):
    secret_key = models.TextField()
    public_key = models.TextField()

    def save(self, *args, **kwargs):
        if not self.secret_key:
            key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            self.secret_key = key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )

            public_key = key.public_key()
            self.public_key = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

        super(ActivityPubPlatformSettings, self).save(*args, **kwargs)
