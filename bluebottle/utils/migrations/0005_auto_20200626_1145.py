# Generated by Django 1.11.15 on 2020-06-26 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0004_auto_20200626_1053'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='translationplatformsettings',
            options={'verbose_name': 'translation settings', 'verbose_name_plural': 'translation settings'},
        ),
        migrations.AlterModelOptions(
            name='translationplatformsettingstranslation',
            options={'default_permissions': (), 'managed': True, 'verbose_name': 'translation settings Translation'},
        ),
        migrations.RemoveField(
            model_name='translationplatformsettingstranslation',
            name='location',
        ),
        migrations.RemoveField(
            model_name='translationplatformsettingstranslation',
            name='location_group',
        ),
        migrations.RemoveField(
            model_name='translationplatformsettingstranslation',
            name='location_groups',
        ),
        migrations.RemoveField(
            model_name='translationplatformsettingstranslation',
            name='locations',
        ),
        migrations.AddField(
            model_name='translationplatformsettingstranslation',
            name='office',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=b'Office'),
        ),
        migrations.AddField(
            model_name='translationplatformsettingstranslation',
            name='office_location',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=b'Office location'),
        ),
        migrations.AddField(
            model_name='translationplatformsettingstranslation',
            name='select_an_office_location',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=b'Select an office location'),
        ),
        migrations.AddField(
            model_name='translationplatformsettingstranslation',
            name='whats_the_location_of_your_office',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=b"What's the location of your office"),
        ),
    ]
