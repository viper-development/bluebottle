# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-01-23 16:31
from __future__ import unicode_literals

from django.db import migrations


def set_stripe_document_default(apps, schema_editor):
    StripePayoutAccount = apps.get_model('payouts', 'StripePayoutAccount')
    StripePayoutAccount.objects.update(document_type='passport')


class Migration(migrations.Migration):

    dependencies = [
        ('payouts', '0019_auto_20190123_1216'),
    ]

    operations = [
        migrations.RunPython(set_stripe_document_default, migrations.RunPython.noop)
    ]
