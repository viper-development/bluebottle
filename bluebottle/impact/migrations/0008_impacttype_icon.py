# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-07-15 14:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('impact', '0007_auto_20200714_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='impacttype',
            name='icon',
            field=models.CharField(blank=True, choices=[(b'people', 'People'), (b'time', 'Time'), (b'money', 'Money'), (b'trees', 'Trees'), (b'animals', 'Animals'), (b'jobs', 'Jobs'), (b'co2', 'C02'), (b'water', 'Water'), (b'plastic', 'plastic')], max_length=20, null=True, verbose_name='icon'),
        ),
    ]
