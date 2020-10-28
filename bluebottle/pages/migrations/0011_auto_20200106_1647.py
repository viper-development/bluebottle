# Generated by Django 1.10.7 on 2017-08-03 14:14

from django.db import migrations

from bluebottle.utils.utils import update_group_permissions


def add_group_permissions(apps, schema_editor):
    group_perms = {
        'Staff': {
            'perms': (
                'add_imagetextitem', 'change_imagetextitem', 'delete_imagetextitem',
                'add_documentitem', 'change_documentitem', 'delete_documentitem',
            )
        }
    }

    update_group_permissions('pages', group_perms, apps)


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0010_auto_20180717_1017'),
    ]

    operations = [
        migrations.RunPython(add_group_permissions)
    ]
