# Generated by Django 1.10.8 on 2017-12-04 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0062_auto_20171128_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logoscontent',
            name='action_text',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
