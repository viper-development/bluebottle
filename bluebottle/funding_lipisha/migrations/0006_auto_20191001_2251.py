# Generated by Django 1.11.15 on 2019-10-01 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funding_lipisha', '0005_auto_20191001_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lipishabankaccount',
            name='address',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='lipishabankaccount',
            name='swift',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name=b'SWIFT/Routing Code'),
        ),
    ]
