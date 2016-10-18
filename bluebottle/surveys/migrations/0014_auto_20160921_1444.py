# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-21 12:44
from __future__ import unicode_literals

from django.db import migrations
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0013_auto_20160921_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='aggregateanswer',
            name='list',
            field=django_extensions.db.fields.json.JSONField(default=b'[]', null=True),
        ),
        migrations.AddField(
            model_name='aggregateanswer',
            name='options',
            field=django_extensions.db.fields.json.JSONField(null=True),
        ),
    ]