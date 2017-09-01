# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-24 16:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0018_auto_20170824_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='is_co_financer',
            field=models.BooleanField(default=False, help_text='Donations by co-financers are shown in a separate list on the project page. These donation will always be visible.', verbose_name='Co-financer'),
        ),
    ]
