# Generated by Django 1.11.15 on 2019-11-07 07:53

from django.db import migrations


def clear_user_dashboard(apps, schema_editor):
    UserDashboardModule = apps.get_model('dashboard', 'UserDashboardModule')
    UserDashboardModule.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('bluebottle_dashboard', '0001_initial'),
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(clear_user_dashboard, migrations.RunPython.noop)
    ]
