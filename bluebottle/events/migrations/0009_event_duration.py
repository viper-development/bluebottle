# Generated by Django 1.11.15 on 2019-08-12 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20190812_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='duration',
            field=models.FloatField(blank=True, null=True, verbose_name='end'),
        ),
    ]
