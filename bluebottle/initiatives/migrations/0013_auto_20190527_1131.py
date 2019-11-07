# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-05-27 09:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0013_auto_20190524_0958'),
        ('initiatives', '0012_merge_20190524_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='initiative',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='geo.Location'),
        ),
        migrations.AlterField(
            model_name='initiative',
            name='status',
            field=django_fsm.FSMField(choices=[(b'created', 'created'), (b'submitted', 'submitted'), (b'needs_work', 'needs work'), (b'approved', 'approved'), (b'closed', 'closed')], default=b'created', max_length=50, protected=True),
        ),
    ]