# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-19 14:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0005_auto_20160919_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, default=datetime.datetime(2016, 9, 19, 14, 9, 46, 140406, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='updated',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, default=datetime.datetime(2016, 9, 19, 14, 9, 58, 435909, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
