# Generated by Django 1.10.8 on 2017-10-30 21:49

from django.db import migrations


def forward(apps, schema_editor):
    Project = apps.get_model('projects', 'Project')
    Project.objects.filter(amount_asked=0, payout_status__isnull=False).update(payout_status=None)


def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0042_merge_20170920_1332'),
    ]

    operations = [
        migrations.RunPython(forward, backward)
    ]

