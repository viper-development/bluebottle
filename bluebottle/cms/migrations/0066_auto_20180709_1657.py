# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-07-09 14:57
from __future__ import unicode_literals

from django.db import migrations

from bluebottle.utils.utils import update_group_permissions


def add_group_permissions(apps, schema_editor):
    group_perms = {
        'Anonymous': {
            'perms': (
                'api_read_page',
            )
        },
        'Authenticated': {
            'perms': (
                'api_read_page',
            )
        },
    }

    update_group_permissions('pages', group_perms, apps)

    group_perms = {
        'Anonymous': {
            'perms': (
                'api_read_newsitem',
            )
        },
        'Authenticated': {
            'perms': (
                'api_read_newsitem',
            )
        },
    }

    update_group_permissions('news', group_perms, apps)


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0065_auto_20180313_1401'),
        ('news', '0007_auto_20180709_1706'),
        ('pages','0009_auto_20180709_1706'),
    ]

    operations = [
        migrations.RunPython(add_group_permissions)
    ]
