# Generated by Django 1.10.8 on 2019-01-30 10:41

from django.db import migrations
from django.db.models import F


def migrate_donation_payout_amounts(apps, schema_editor):
    Donation = apps.get_model('donations', 'Donation')
    Donation.objects.update(payout_amount=F('amount'), payout_amount_currency=F('amount_currency'))


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0009_auto_20190130_1140'),
    ]

    operations = [
        migrations.RunPython(migrate_donation_payout_amounts, migrations.RunPython.noop)
    ]
