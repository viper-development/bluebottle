# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-11-03 09:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0003_auto_20180727_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailplatformsettings',
            name='email_logo',
            field=models.ImageField(blank=True, null=True, upload_to=b'site_content/'),
        ),
    ]
