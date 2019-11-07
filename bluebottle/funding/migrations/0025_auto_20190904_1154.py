# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-09-04 09:54
from __future__ import unicode_literals

import bluebottle.utils.fields
from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('funding', '0024_bankpaymentprovider'),
    ]

    operations = [
        migrations.CreateModel(
            name='LegacyPayment',
            fields=[
                ('payment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='funding.Payment')),
                ('method', models.CharField(max_length=100)),
                ('data', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=('funding.payment',),
        ),
        migrations.AddField(
            model_name='donation',
            name='payout_amount',
            field=bluebottle.utils.fields.MoneyField(currency_choices=[(b'EUR', b'Euro')], decimal_places=2, default=Decimal('0.0'), max_digits=12),
        ),
        migrations.AddField(
            model_name='donation',
            name='payout_amount_currency',
            field=djmoney.models.fields.CurrencyField(choices=[(b'EUR', b'Euro')], default=b'EUR', editable=False, max_length=3),
        ),
    ]