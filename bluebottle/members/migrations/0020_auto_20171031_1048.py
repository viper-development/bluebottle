# Generated by Django 1.10.8 on 2017-10-31 09:48

from django.db import migrations


def rename_full_member_permission(apps, schema_editor):
    Permission = apps.get_model('auth', 'Permission')

    perm = Permission.objects.get(codename='api_read_full_member')

    perm.name = 'Can view full members through the API'
    perm.save()



class Migration(migrations.Migration):

    dependencies = [
        ('members', '0019_auto_20170824_1812'),
    ]

    operations = [
        migrations.RunPython(rename_full_member_permission)
    ]
