# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-09-19 12:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='custom_message',
            field=models.TextField(blank=True, null=True),
        ),
    ]
