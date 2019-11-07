# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-08-26 13:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('funding', '0023_bankpayoutaccount'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankPaymentProvider',
            fields=[
                ('paymentprovider_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='funding.PaymentProvider')),
            ],
            options={
                'abstract': False,
            },
            bases=('funding.paymentprovider',),
        ),
    ]