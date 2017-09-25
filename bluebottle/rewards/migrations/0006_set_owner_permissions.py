# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-23 09:31
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth.models import Permission, Group

from bluebottle.utils.utils import update_group_permissions


def set_owner_permissions(apps, schema_editor):
    group_perms = {
        'Anonymous': {
            'perms': ('api_read_reward', )
        },
        'Authenticated': {
            'perms': (
                'api_read_reward', 'api_add_own_reward', 'api_change_own_reward',
                'api_delete_own_reward'
            )
        }
    }
    update_group_permissions('rewards', group_perms, apps)

    authenticated = Group.objects.get(name='Authenticated')
    for perm in (
        'api_add_reward', 'api_change_reward', 'api_delete_reward',
        ):
        authenticated.permissions.remove(
            Permission.objects.get(
                codename=perm, content_type__app_label='rewards'
            )
        )


class Migration(migrations.Migration):

    dependencies = [
        ('rewards', '0005_auto_20170823_1131'),
    ]

    operations = [
        migrations.RunPython(set_owner_permissions)
    ]