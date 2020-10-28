# Generated by Django 1.10.8 on 2018-01-21 19:02

import bluebottle.utils.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0065_auto_20180121_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectcreatetemplate',
            name='default_amount_asked',
            field=bluebottle.utils.fields.MoneyField(blank=True, currency_choices="[('EUR', u'Euro')]", decimal_places=2, default=None, max_digits=12, null=True),
        ),
    ]
