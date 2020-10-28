# Generated by Django 1.11.15 on 2019-11-08 07:19

from django.db import migrations


def fix_payout_status(apps, schema_editor):
    Payout = apps.get_model('funding', 'Payout')
    Payout.objects.filter(status='needs_approval').update(status='new')
    Payout.objects.filter(status='scheduled').update(status='new')
    Payout.objects.filter(status='re_scheduled').update(status='started')
    Payout.objects.filter(status='in_progress').update(status='started')
    Payout.objects.filter(status='partial').update(status='started')
    Payout.objects.filter(status='success').update(status='succeeded')
    # Payout.objects.filter(status='failed').update(status='failed')


class Migration(migrations.Migration):

    dependencies = [
        ('funding', '0042_auto_20191104_1154'),
    ]

    operations = [
        migrations.RunPython(fix_payout_status, migrations.RunPython.noop)
    ]
