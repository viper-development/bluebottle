# Generated by Django 1.10.8 on 2018-01-19 11:31

import bluebottle.utils.fields
from decimal import Decimal
from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0061_auto_20180118_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectcreatetemplate',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='projectcreatetemplate',
            name='image',
            field=models.ImageField(null=True, upload_to=b''),
        ),
        migrations.AlterField(
            model_name='projectcreatetemplate',
            name='amount',
            field=bluebottle.utils.fields.MoneyField(currency_choices="[('EUR', u'Euro')]", decimal_places=2, default=Decimal('0.0'), max_digits=12),
        ),
        migrations.AlterField(
            model_name='projectcreatetemplate',
            name='amount_currency',
            field=djmoney.models.fields.CurrencyField(choices=[(b'EUR', 'Euro')], default='EUR', editable=False, max_length=3),
        ),
    ]
