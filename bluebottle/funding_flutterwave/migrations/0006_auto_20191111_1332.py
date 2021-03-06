# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-11-11 12:19
from __future__ import unicode_literals

from django.db import migrations
from bluebottle.utils.utils import update_group_permissions


def add_group_permissions(apps, schema_editor):
    group_perms = {
        'Staff': {
            'perms': (
                'add_flutterwavebankaccount',
                'change_flutterwavebankaccount',
            )
        },
    }

    update_group_permissions('funding_flutterwave', group_perms, apps)


class Migration(migrations.Migration):

    dependencies = [
        ('funding_flutterwave', '0005_auto_20191002_0903'),
    ]

    operations = [
        migrations.RunPython(add_group_permissions)
    ]
