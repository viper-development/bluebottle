# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-10-23 17:58
from __future__ import unicode_literals

import bluebottle.utils.fields
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0042_merge_20170920_1332'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectPlatformSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update', models.DateTimeField(auto_now=True)),
                ('project_create_types', multiselectfield.MultiSelectField(choices=[(b'sourcing', 'Sourcing'), (b'funding', 'Funding')], max_length=100)),
                ('project_create_flow', models.CharField(choices=[(b'combined', 'Combined'), (b'choice', 'Choice')], max_length=100)),
                ('project_suggestions', models.BooleanField(default=True)),
                ('project_contact_method', models.CharField(choices=[(b'mail', 'E-mail'), (b'phone', 'Choose')], max_length=100)),
            ],
            options={
                'verbose_name': 'Project Settings',
                'verbose_name_plural': 'Project Settings',
            },
        ),
        migrations.CreateModel(
            name='ProjectSearchFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[(b'location', 'Location'), (b'theme', 'Theme'), (b'skill', 'Skill'), (b'date', 'Date'), (b'status', 'Status'), (b'type', 'Type')], max_length=100)),
                ('default', models.CharField(blank=True, max_length=100, null=True)),
                ('values', models.CharField(blank=True, help_text='Comma separated list of possible values', max_length=500, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='projectplatformsettings',
            name='search_filters',
            field=models.ManyToManyField(to='projects.ProjectSearchFilter'),
        ),
    ]
