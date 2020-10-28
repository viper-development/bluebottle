# Generated by Django 1.11.15 on 2019-05-24 09:59

from django.db import migrations

from bluebottle.utils.utils import update_group_permissions


def add_group_permissions(apps, schema_editor):
    group_perms = {
        'Staff': {
            'perms': (
                'add_event', 'change_event', 'delete_event',
            )
        },
        'Anonymous': {
            'perms': (
                'api_read_event',
            )
        },
        'Authenticated': {
            'perms': (
                'api_read_event',
                'api_add_own_event',
                'api_change_own_event',
                'api_delete_own_event',
            )
        }
    }

    update_group_permissions('events', group_perms, apps)


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            add_group_permissions,
            migrations.RunPython.noop
        )
    ]
