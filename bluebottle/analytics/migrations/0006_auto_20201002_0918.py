# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-10-02 07:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0005_auto_20180424_1205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analyticsadapter',
            name='analytics_settings',
        ),
        migrations.AlterModelOptions(
            name='analyticsplatformsettings',
            options={'verbose_name': 'reporting platform settings', 'verbose_name_plural': 'reporting platform settings'},
        ),
        migrations.AddField(
            model_name='analyticsplatformsettings',
            name='user_base',
            field=models.PositiveIntegerField(null=True, verbose_name='Number of employees or number of users that could access the platform'),
        ),
        migrations.DeleteModel(
            name='AnalyticsAdapter',
        ),
    ]