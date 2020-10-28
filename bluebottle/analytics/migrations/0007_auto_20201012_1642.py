# Generated by Django 1.11.17 on 2020-10-12 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0006_auto_20201002_0918'),
    ]

    operations = [
        migrations.AddField(
            model_name='analyticsplatformsettings',
            name='platform_type',
            field=models.CharField(choices=[('corporate', 'Corporate'), ('programs', 'Programs'), ('civic', 'Civic')], default='corporate', max_length=10, verbose_name='platform type'),
        ),
        migrations.AlterField(
            model_name='analyticsplatformsettings',
            name='fiscal_month_offset',
            field=models.PositiveIntegerField(default=0, help_text='This could be used in reporting.', verbose_name='Fiscal year offset'),
        ),
        migrations.AlterField(
            model_name='analyticsplatformsettings',
            name='user_base',
            field=models.PositiveIntegerField(blank=True, help_text='Number of employees or number of users that could access the platform.', null=True, verbose_name='User base'),
        ),
    ]
