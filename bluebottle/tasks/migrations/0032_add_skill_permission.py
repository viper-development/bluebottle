# Generated by Django 1.10.7 on 2017-08-29 07:33

from django.db import migrations

from bluebottle.utils.utils import update_group_permissions


def add_group_permissions(apps, schema_editor):
    group_perms = {
        'Anonymous': {
            'perms': ('api_read_skill',)
        },
        'Authenticated': {
            'perms': ('api_read_skill', )
        }
    }
    update_group_permissions('tasks', group_perms, apps)




class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0031_set_owner_permissions'),
    ]

    operations = [
        migrations.RunPython(add_group_permissions)
    ]
