# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-01-06 15:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fluent_contents', '0001_initial'),
        ('pages', '0010_auto_20180717_1017'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionItem',
            fields=[
                ('contentitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fluent_contents.ContentItem')),
                ('link', models.CharField(max_length=200, verbose_name='link')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
            ],
            options={
                'db_table': 'contentitem_pages_actionitem',
                'verbose_name': 'Call to action',
                'verbose_name_plural': 'Call to actions',
            },
            bases=('fluent_contents.contentitem',),
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='page',
            name='language',
            field=models.CharField(choices=[(b'nl', b'Dutch'), (b'en', b'English')], max_length=5, verbose_name='language'),
        ),
        migrations.AlterField(
            model_name='page',
            name='publication_date',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, help_text="To go live, status must be 'Published'.", null=True, verbose_name='publication date'),
        ),
    ]
