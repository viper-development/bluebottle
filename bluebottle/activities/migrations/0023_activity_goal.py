# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-06-24 08:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('impact', '0001_initial'),
        ('activities', '0022_activity_video_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='goal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='impact.ImpactGoal'),
        ),
    ]
