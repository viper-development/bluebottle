# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-11-27 11:08
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('payments', '0006_auto_20181115_1321'),
    ]

    operations = [
        migrations.CreateModel(
            name='StripePayment',
            fields=[
                ('payment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='payments.Payment')),
                ('source_token', models.CharField(help_text='Source token obtained in front-end.', max_length=100, null=True)),
                ('charge_token', models.CharField(help_text='Charge token at Stripe.', max_length=100, null=True)),
                ('amount', models.IntegerField(help_text='Payment amount in smallest units (e.g. cents).', null=True)),
                ('description', models.CharField(max_length=300, null=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
            options={
                'abstract': False,
            },
            bases=('payments.payment',),
        ),
    ]
