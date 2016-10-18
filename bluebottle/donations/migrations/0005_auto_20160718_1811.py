# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-18 16:11
from __future__ import unicode_literals

import bluebottle.utils.fields
from decimal import Decimal
from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0004_auto_20160523_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='amount_currency',
            field=djmoney.models.fields.CurrencyField(choices=[(b'EUR', b'Euro')], default=b'EUR', editable=False, max_length=3),
        ),
        migrations.AlterField(
            model_name='donation',
            name='amount',
            field=bluebottle.utils.fields.MoneyField(currency_choices=[(b'EUR', b'Euro')], decimal_places=2, default=Decimal('0.0'), default_currency=b'EUR', max_digits=12, verbose_name='Amount'),
        ),
    ]
