# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-15 15:01
from __future__ import unicode_literals

from django.db import migrations
import select_multiple_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0013_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='currencies',
            field=select_multiple_field.models.SelectMultipleField(choices=[(b'EUR', 'Euro')], default=[], max_length=100, null=True),
        ),
    ]
