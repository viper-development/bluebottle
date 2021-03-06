# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-07-27 09:22
from __future__ import unicode_literals

from django.db import migrations


def create_settings(apps, schema_editor):
    MailPlatformSettings = apps.get_model('mails', 'MailPlatformSettings')
    if not MailPlatformSettings.objects.count():
        MailPlatformSettings.objects.create()


def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0002_auto_20171211_1117'),
    ]

    operations = [
        migrations.RunPython(create_settings, backward)
    ]
