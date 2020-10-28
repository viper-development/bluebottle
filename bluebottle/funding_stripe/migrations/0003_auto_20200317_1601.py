# Generated by Django 1.11.15 on 2020-03-17 15:01

from django.db import migrations, models
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('funding_stripe', '0002_auto_20191111_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='stripepayoutaccount',
            name='eventually_due',
            field=django_extensions.db.fields.json.JSONField(default=[], null=True),
        ),
        migrations.AlterField(
            model_name='externalaccount',
            name='account_id',
            field=models.CharField(help_text="Starts with 'ba_...'", max_length=40),
        ),
        migrations.AlterField(
            model_name='stripepayoutaccount',
            name='account_id',
            field=models.CharField(help_text="Starts with 'acct_...'", max_length=40),
        ),
    ]
