# Generated by Django 1.11.15 on 2019-06-04 14:15

import bluebottle.utils.fields
from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('payouts', '0022_auto_20190211_1452'),
        ('funding', '0005_auto_20190604_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='funding',
            name='account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='payouts.PayoutAccount'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='amount',
            field=bluebottle.utils.fields.MoneyField(currency_choices="[('EUR', u'Euro')]", decimal_places=2, default=Decimal('0.0'), max_digits=12),
        ),
        migrations.AlterField(
            model_name='donation',
            name='amount_currency',
            field=djmoney.models.fields.CurrencyField(choices=[(b'EUR', 'Euro')], default='EUR', editable=False, max_length=3),
        ),
        migrations.AlterField(
            model_name='funding',
            name='target',
            field=bluebottle.utils.fields.MoneyField(currency_choices="[('EUR', u'Euro')]", decimal_places=2, default=Decimal('0.0'), max_digits=12),
        ),
        migrations.AlterField(
            model_name='funding',
            name='target_currency',
            field=djmoney.models.fields.CurrencyField(choices=[(b'EUR', 'Euro')], default='EUR', editable=False, max_length=3),
        ),
    ]
