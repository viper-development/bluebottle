# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-15 15:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallposts', '0002_auto_20161115_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediawallpostphoto',
            name='results_page',
            field=models.BooleanField(default=True),
        ),
    ]
