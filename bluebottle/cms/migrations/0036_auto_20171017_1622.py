# Generated by Django 1.10.8 on 2017-10-17 14:22

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0035_auto_20171017_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectscontent',
            name='from_homepage',
            field=models.BooleanField(default=False),
        ),
    ]
