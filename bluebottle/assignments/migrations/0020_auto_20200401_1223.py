# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-04-01 10:23
from __future__ import unicode_literals

import bluebottle.files.fields
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0006_auto_20200401_1223'),
        ('assignments', '0019_remove_applicant_document'),
    ]

    operations = [
        migrations.RenameField(
            model_name='applicant',
            old_name='private_document',
            new_name='document'
        ),
    ]
