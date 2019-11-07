# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-08-14 13:41
from __future__ import unicode_literals

import bluebottle.fsm
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0007_auto_20190710_0851'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='review_status',
            field=bluebottle.fsm.FSMField(default=b'draft', max_length=20),
        ),
        migrations.AlterField(
            model_name='activity',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='activity',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='status',
            field=bluebottle.fsm.FSMField(default=b'draft', max_length=20),
        ),
        migrations.AlterField(
            model_name='contribution',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]