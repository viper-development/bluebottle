# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-10-22 09:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('funding', '0038_auto_20191014_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='payout',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='donations', to='funding.Payout'),
        ),
    ]
