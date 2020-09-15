# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-07 08:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager

from fluent_contents.models.managers import ContentItemManager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fluent_contents', '0001_initial'),
        ('projects', '0015_auto_20161207_0900'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectImagesContent',
            fields=[
                ('contentitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fluent_contents.ContentItem')),
                ('title', models.CharField(blank=True, max_length=63, null=True)),
                ('sub_title', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('action_text', models.CharField(blank=True, default='Check out our projects', max_length=100, null=True)),
                ('action_link', models.CharField(blank=True, default=b'/projects', max_length=100, null=True)),
            ],
            options={
                'db_table': 'contentitem_cms_projectimagescontent',
                'verbose_name': 'Project Images',
            },
            bases=('fluent_contents.contentitem',),
            managers=[
                ('objects', ContentItemManager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projects', models.ManyToManyField(to='projects.Project')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectsContent',
            fields=[
                ('contentitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fluent_contents.ContentItem')),
                ('title', models.CharField(blank=True, max_length=63, null=True)),
                ('sub_title', models.CharField(blank=True, max_length=100, null=True)),
                ('action', models.CharField(max_length=255)),
                ('action_text', models.CharField(max_length=255)),
                ('projects', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.Projects')),
            ],
            options={
                'db_table': 'contentitem_cms_projectscontent',
                'verbose_name': 'Projects',
            },
            bases=('fluent_contents.contentitem',),
            managers=[
                ('objects', ContentItemManager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
                ('quote', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Quotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='QuotesContent',
            fields=[
                ('contentitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fluent_contents.ContentItem')),
                ('title', models.CharField(blank=True, max_length=63, null=True)),
                ('sub_title', models.CharField(blank=True, max_length=100, null=True)),
                ('quotes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Quotes')),
            ],
            options={
                'db_table': 'contentitem_cms_quotescontent',
                'verbose_name': 'Quotes',
            },
            bases=('fluent_contents.contentitem',),
            managers=[
                ('objects', ContentItemManager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ResultPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('slug', models.SlugField(max_length=200, verbose_name='Slug')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[(b'manual', 'Manual input'), (b'people_involved', 'People involved'), (b'projects_realized', 'Projects realised'), (b'tasks_realized', 'Tasks realised'), (b'donated_total', 'Donated total'), (b'projects_online', 'Projects Online'), (b'votes_cast', 'Votes casts')], max_length=40)),
                ('title', models.CharField(max_length=63)),
                ('value', models.CharField(blank=True, help_text="Use this for 'manual' input or the override the calculated value.", max_length=63, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='StatsContent',
            fields=[
                ('contentitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fluent_contents.ContentItem')),
                ('title', models.CharField(blank=True, max_length=63, null=True)),
                ('sub_title', models.CharField(blank=True, max_length=100, null=True)),
                ('stats', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Stats')),
            ],
            options={
                'db_table': 'contentitem_cms_statscontent',
                'verbose_name': 'Platform Statistics',
            },
            bases=('fluent_contents.contentitem',),
            managers=[
                ('objects', ContentItemManager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='SurveyContent',
            fields=[
                ('contentitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fluent_contents.ContentItem')),
                ('title', models.CharField(blank=True, max_length=63, null=True)),
                ('sub_title', models.CharField(blank=True, max_length=100, null=True)),
                ('survey', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='surveys.Survey')),
            ],
            options={
                'db_table': 'contentitem_cms_surveycontent',
                'verbose_name': 'Platform Results',
            },
            bases=('fluent_contents.contentitem',),
            managers=[
                ('objects', ContentItemManager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='stat',
            name='stats',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Stats'),
        ),
        migrations.AddField(
            model_name='quote',
            name='quotes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Quotes'),
        ),
    ]
