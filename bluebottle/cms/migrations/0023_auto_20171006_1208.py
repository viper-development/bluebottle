# Generated by Django 1.10.8 on 2017-10-06 10:08

from django.db import migrations

from bluebottle.utils.utils import update_group_permissions


def add_group_permissions(apps, schema_editor):
    group_perms = {
        'Staff': {
            'perms': ('change_homepage', )
        },
        'Authenticated': {
            'perms': ('api_read_homepage', )
        },
        'Anonymous': {
            'perms': ('api_read_homepage', )
        }

    }

    update_group_permissions('cms', group_perms, apps)




class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20171006_1155'),
    ]

    operations = [
        migrations.RunPython(add_group_permissions)
    ]
