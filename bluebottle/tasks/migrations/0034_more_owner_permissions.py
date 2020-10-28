# Generated by Django 1.10.7 on 2017-08-31 09:02

from django.db import migrations

from bluebottle.utils.utils import update_group_permissions


def set_owner_permissions(apps, schema_editor):
    group_perms = {
        'Staff': {
            'perms': ('api_read_taskmember_resume', )
        },
        'Anonymous': {
            'perms': ('api_read_task', 'api_read_skill')
        },
        'Authenticated': {
            'perms': (
                'api_read_task', 'api_add_own_task',
                'api_change_own_task', 'api_delete_own_task',
                'api_read_taskmember', 'api_add_taskmember',
                'api_add_own_taskmember', 'api_read_own_taskmember',
                'api_change_own_taskmember', 'api_delete_own_taskmember',
                'api_read_own_taskmember_resume',
                'api_read_skill'
            )
        }
    }
    update_group_permissions('tasks', group_perms, apps)


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0033_merge_20170830_1106'),
    ]

    operations = [
        migrations.RunPython(set_owner_permissions)
    ]
