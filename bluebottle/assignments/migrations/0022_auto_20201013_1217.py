# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-10-13 10:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0021_auto_20201012_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='online_meeting_url',
            field=models.TextField(blank=True, null=True, verbose_name='Online Meeting URL'),
        ),
    ]