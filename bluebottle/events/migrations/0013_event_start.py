# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-02-17 10:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_auto_20200217_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='start',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Start'),
        ),
    ]