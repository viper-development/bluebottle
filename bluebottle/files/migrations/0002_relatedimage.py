# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-10-14 11:27
from __future__ import unicode_literals

import bluebottle.files.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('image', bluebottle.files.fields.ImageField(on_delete=django.db.models.deletion.CASCADE, to='files.Image')),
            ],
        ),
    ]
