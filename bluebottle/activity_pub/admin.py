from urlparse import urlparse
import json
import requests
import httpsig

from django.utils import timezone

from django.contrib import admin
from django.db import connection
from django import forms

from bluebottle.activity_pub.models import Server
from bluebottle.activity_pub.models import ActivityPubPlatformSettings


class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        # Mind you these fields are also set in MemberAdmin.add_fieldsets
        fields = ('domain', )


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain', 'public_key')
    add_form = ServerForm

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = self.add_form

        return super(ServerAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            settings = ActivityPubPlatformSettings.objects.get()

            data = {
                'data': {
                    'type': 'servers',
                    'attributes': Server.local_properties
                }
            }
            date = timezone.now().isoformat()
            path = '/api/activity-pub/request'

            url = obj.domain + path

            signer = httpsig.HeaderSigner(
                connection.tenant.domain_url,
                settings.secret_key,
                algorithm="rsa-sha256",
                headers=['(request-target)', 'host', 'date']
            )

            signed_headers_dict = signer.sign(
                {
                    'Date': date,
                    'Host': urlparse(obj.domain).netloc
                },
                method='POST',
                path=path

            )

            response = requests.post(
                url,
                data=json.dumps(data),
                headers={
                    'Content-Type': 'application/vnd.api+json',
                    'Accept': 'application/vnd.api+json',
                    'Date': date,
                    'Authorization': signed_headers_dict['authorization']
                }
            )

            for key, value in response.json()['data']['attributes']['local-properties'].items():
                setattr(obj, key, value)

            super(ServerAdmin, self).save_model(request, obj, form, change)
