# Generated by Django 1.11.15 on 2019-06-05 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_event_is_online'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='end'),
        ),
        migrations.AlterField(
            model_name='event',
            name='registration_deadline',
            field=models.DateTimeField(blank=True, null=True, verbose_name='registration deadline'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='start'),
        ),
    ]
