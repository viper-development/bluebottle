# Generated by Django 1.10.8 on 2017-12-28 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0033_merge_20170124_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='active',
            field=models.BooleanField(default=False, help_text='Should this survey be used in emails?'),
        ),
    ]
