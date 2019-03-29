# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-12-03 10:36
from __future__ import unicode_literals

import bluebottle.utils.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payouts', '0008_auto_20181129_1451'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayoutDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', bluebottle.utils.fields.PrivateFileField(max_length=110, upload_to=b'private/projects/documents')),
                ('created', models.DateField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateField(auto_now=True, verbose_name='updated')),
                ('deleted', models.DateTimeField(blank=True, null=True, verbose_name='deleted')),
                ('ip_address', models.GenericIPAddressField(blank=True, default=None, null=True, verbose_name='IP address')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('payout_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='payouts.PayoutAccount')),
            ],
            options={
                'verbose_name': 'payout document',
                'verbose_name_plural': 'payout documents',
            },
        ),
    ]