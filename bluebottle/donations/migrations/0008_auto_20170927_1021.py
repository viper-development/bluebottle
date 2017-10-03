# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-09-27 08:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0007_donation_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='name',
            field=models.CharField(blank=True, db_index=True, max_length=200, null=True, verbose_name='Name of donor'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='reward',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='donations', to='rewards.Reward', verbose_name='Reward'),
        ),
    ]