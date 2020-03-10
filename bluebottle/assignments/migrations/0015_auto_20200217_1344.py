# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-02-17 12:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0014_auto_20200206_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='date',
            field=models.DateTimeField(blank=True, help_text='Either the start date or the deadline of the task', null=True, verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='preparation',
            field=models.FloatField(blank=True, help_text='Only effective when task takes place on specific date.', null=True, verbose_name='number of hours required for preparation'),
        ),
    ]