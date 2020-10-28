# Generated by Django 1.10.8 on 2018-03-30 09:11

from django.conf import settings
from django.db import migrations, connection
from django.utils.translation import activate, _trans, ugettext as _

from tenant_extras.middleware import tenant_translation

from bluebottle.clients.utils import LocalTenant
from bluebottle.utils.utils import get_languages


def translate_geo(apps, schema_editor):
    Client = apps.get_model('clients', 'Client')
    tenant = Client.objects.get(schema_name=connection.tenant.schema_name)

    with LocalTenant(tenant):
        languages = get_languages()
        for model in ['Region', 'SubRegion', 'Country']:
            Model = apps.get_model('geo', model)
            ModelTranslation = apps.get_model('geo', f'{model}Translation')

            for object in Model.objects.all():
                for (language, _long_language) in languages:
                    activate(language)
                    _trans._active.value = tenant_translation(language, tenant.client_name)
                    ModelTranslation.objects.create(
                        master_id=object.pk,
                        language_code=language,
                        _name=_(object.name),
                    )


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0005_translate_geo'),
    ]

    operations = [
        migrations.RunPython(translate_geo)
    ]
