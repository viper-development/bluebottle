# Generated by Django 1.11.15 on 2020-02-05 16:10

from django.db import migrations


def update_refund_status(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Funding = apps.get_model('funding', 'Funding')
    Donation = apps.get_model('funding', 'Donation')

    for funding in Funding.objects.filter(status='refunded'):
        Donation.objects.filter(activity=funding, status='refunded').update(
            status='activity_refunded'
        )

class Migration(migrations.Migration):

    dependencies = [
        ('funding', '0051_funding_update_contribution_date'),
    ]

    operations = [
        migrations.RunPython(update_refund_status),
    ]
