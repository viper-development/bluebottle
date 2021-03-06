# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-10-06 09:18
from __future__ import unicode_literals

from django.db import migrations, models
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0020_add_group_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('api_read_homepage', 'Can view homepages through the API'), ('api_add_homepage', 'Can add homepages through the API'), ('api_change_homepage', 'Can change homepages through the API'), ('api_delete_homepage', 'Can delete homepages through the API')),
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
    ]
