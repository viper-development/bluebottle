# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-21 14:37
from __future__ import unicode_literals

from django.db import migrations, connection

def forward(apps, schema_editor):

    with connection.cursor() as cursor:
        cursor.execute("SELECT applied FROM django_migrations WHERE name='0010_fix_export_permissions_migration'")
        start_date = cursor.fetchone()[0]
        cursor.execute("SELECT applied FROM django_migrations WHERE name='0027_auto_20170602_2240'")
        end_date = cursor.fetchone()[0]

    ProjectPhaseLog = apps.get_model('projects', 'ProjectPhaseLog')

    for status_log in ProjectPhaseLog.objects.filter(start__range=(start_date, end_date)):
        new_date = status_log.project.deadline if status_log.project.deadline else status_log.project.created
        ProjectPhaseLog.objects.filter(id=status_log.id).update(start=new_date)

def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0010_fix_export_permissions_migration'),
        ('projects', '0027_auto_20170602_2240'),
        ('projects', '0030_rename_account_bic_20170705_1221'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
