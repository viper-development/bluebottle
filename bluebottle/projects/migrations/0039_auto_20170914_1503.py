# Generated by Django 1.10.7 on 2017-09-14 13:03

import bluebottle.utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0038_longer_account_details_20170914_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(db_index=True, max_length=255, unique=True, verbose_name='title'),
        ),
    ]
