# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-07-08 12:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segments', '0003_auto_20200706_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='segmenttype',
            name='enable_search',
            field=models.BooleanField(default=False, verbose_name='Enable search filters.'),
        ),
        migrations.AlterField(
            model_name='segmenttype',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is active'),
        ),
    ]