# Generated by Django 1.11.15 on 2018-09-07 09:32

from django.db import migrations, connection

from bluebottle.utils.utils import update_group_permissions

from bluebottle.clients import properties
from bluebottle.clients.models import Client
from bluebottle.clients.utils import LocalTenant


def add_group_permissions(apps, schema_editor):
    tenant = Client.objects.get(schema_name=connection.tenant.schema_name)
    with LocalTenant(tenant):
        group_perms = {
            'Anonymous': {
                'perms': ('api_read_terms', ) if not properties.CLOSED_SITE else ()
            }
        }

        update_group_permissions('terms', group_perms, apps)


class Migration(migrations.Migration):

    dependencies = [
        ('terms', '0002_auto_20180907_1132'),
    ]

    operations = [
        migrations.RunPython(add_group_permissions)
    ]
