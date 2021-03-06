# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-09-15 08:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0042_migrate_tasks_to_activities'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='author',
        ),
        migrations.RemoveField(
            model_name='task',
            name='project',
        ),
        migrations.RemoveField(
            model_name='task',
            name='skill',
        ),
        migrations.RemoveField(
            model_name='taskfile',
            name='author',
        ),
        migrations.RemoveField(
            model_name='taskfile',
            name='task',
        ),
        migrations.RemoveField(
            model_name='taskmember',
            name='member',
        ),
        migrations.RemoveField(
            model_name='taskmember',
            name='task',
        ),
        migrations.RemoveField(
            model_name='taskmemberstatuslog',
            name='task_member',
        ),
        migrations.RemoveField(
            model_name='taskstatuslog',
            name='task',
        ),
        migrations.AlterModelOptions(
            name='skill',
            options={'ordering': ['translations__name'], 'permissions': (('api_read_skill', 'Can view skills through the API'),), 'verbose_name': 'Skill', 'verbose_name_plural': 'Skills'},
        ),
        migrations.AlterModelOptions(
            name='skilltranslation',
            options={'default_permissions': (), 'managed': True, 'verbose_name': 'Skill Translation'},
        ),
        migrations.AlterField(
            model_name='skill',
            name='expertise',
            field=models.BooleanField(default=True, help_text='Is this skill expertise based, or could anyone do it?', verbose_name='expertise based'),
        ),
        migrations.AlterUniqueTogether(
            name='skilltranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.DeleteModel(
            name='Task',
        ),
        migrations.DeleteModel(
            name='TaskFile',
        ),
        migrations.DeleteModel(
            name='TaskMember',
        ),
        migrations.DeleteModel(
            name='TaskMemberStatusLog',
        ),
        migrations.DeleteModel(
            name='TaskStatusLog',
        ),
    ]
