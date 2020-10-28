# Generated by Django 1.11.15 on 2019-09-09 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0007_auto_20190909_1519'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignment',
            old_name='deadline',
            new_name='end_date',
        ),
        migrations.AddField(
            model_name='assignment',
            name='end_date_type',
            field=models.CharField(choices=[(b'redirect', 'Redirect'), (b'popup', 'Popup')], default=None, help_text='Either the deadline or the date it will take place.', max_length=50, null=True, verbose_name='end date'),
        ),
    ]
