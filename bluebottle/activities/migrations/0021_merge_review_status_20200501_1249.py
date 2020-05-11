# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-05-01 10:49
from __future__ import unicode_literals

from django.db import migrations
from django.db.models import F


def merge_review_status(apps, schema_editor):
    Activity = apps.get_model('activities', 'Activity')
    Activity.objects.filter(status='in_review').update(status=F('review_status'))
    Activity.objects.filter(review_status='closed').update(status='rejected')


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0020_auto_20200224_1005'),
    ]

    operations = [
        migrations.RunPython(merge_review_status, migrations.RunPython.noop)
    ]
