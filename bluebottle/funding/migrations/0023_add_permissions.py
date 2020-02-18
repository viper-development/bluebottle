# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-08-28 07:04
from __future__ import unicode_literals

from django.db import migrations, connection

from bluebottle.utils.utils import update_group_permissions

from bluebottle.clients import properties
from bluebottle.clients.models import Client
from bluebottle.clients.utils import LocalTenant


def add_group_permissions(apps, schema_editor):
    tenant = Client.objects.get(schema_name=connection.tenant.schema_name)
    with LocalTenant(tenant):
        group_perms = {
            'Staff': {
                'perms': (
                    'add_funding', 'change_funding', 'delete_funding',
                )
            },
            'Anonymous': {
                'perms': ('api_read_funding', ) if not properties.CLOSED_SITE else ()
            },
            'Authenticated': {
                'perms': (
                    'api_read_funding',
                    'api_add_own_funding',
                    'api_change_own_funding',
                    'api_delete_own_funding',
                )
            }
        }

        update_group_permissions('funding', group_perms, apps)


class Migration(migrations.Migration):

    dependencies = [
        ('funding', '0022_auto_20190804_1022'),
    ]

    operations = [
        migrations.RunPython(
            add_group_permissions,
            migrations.RunPython.noop
        )
    ]
