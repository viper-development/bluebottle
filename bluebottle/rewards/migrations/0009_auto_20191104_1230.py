# Generated by Django 1.11.15 on 2019-11-04 11:30

import bluebottle.utils.fields
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rewards', '0008_auto_20170914_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='reward',
            name='new_reward_id',
            field=models.IntegerField(null=True),
        ),
    ]
