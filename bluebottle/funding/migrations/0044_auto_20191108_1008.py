# Generated by Django 1.11.15 on 2019-11-08 09:08

from django.db import migrations


def fix_funding_matching_currencies(apps, schema_editor):
    Funding = apps.get_model('funding', 'Funding')
    for funding in Funding.objects.filter(amount_matching__gt=0):
        if funding.amount_matching.currency != funding.target.currency:
            funding.amount_matching.currency = funding.target.currency
            funding.save()


class Migration(migrations.Migration):

    dependencies = [
        ('funding', '0043_auto_20191108_0819'),
    ]

    operations = [
        migrations.RunPython(fix_funding_matching_currencies, migrations.RunPython.noop)
    ]
