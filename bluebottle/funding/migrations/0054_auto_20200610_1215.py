# Generated by Django 1.11.15 on 2020-06-10 10:15

import bluebottle.files.fields
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('funding', '0053_auto_20200320_1457'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plainpayoutaccount',
            name='document',
        ),
        migrations.AddField(
            model_name='plainpayoutaccount',
            name='document',
            field=bluebottle.files.fields.PrivateDocumentField(blank=True, null=True,
                                                               on_delete=django.db.models.deletion.CASCADE,
                                                               to='files.PrivateDocument'),
        ),
    ]
