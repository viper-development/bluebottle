# Generated by Django 1.10.2 on 2016-11-15 15:01

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('payments_docdata', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='docdatatransaction',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
