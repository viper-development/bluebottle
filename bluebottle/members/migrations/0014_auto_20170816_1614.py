# Generated by Django 1.10.7 on 2017-08-16 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0013_merge_20170811_1500'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'permissions': (('api_read_member', 'Can view members through the API'), ('api_read_full_member', 'Can view members through the API'), ('api_add_member', 'Can add members through the API'), ('api_change_member', 'Can change members through the API'), ('api_delete_member', 'Can delete members through the API')), 'verbose_name': 'member', 'verbose_name_plural': 'members'},
        ),
    ]
