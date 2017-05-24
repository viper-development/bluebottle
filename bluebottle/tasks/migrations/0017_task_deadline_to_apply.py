# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-19 14:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0016_auto_20161208_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='deadline_to_apply',
            field=models.FloatField(help_text='Deadline to apply', null=True, verbose_name='deadline_to_apply'),
        ),
    ]