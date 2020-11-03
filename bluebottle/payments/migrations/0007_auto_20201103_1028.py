# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-11-03 09:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0006_auto_20181115_1321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderpayment',
            name='authorization_action',
        ),
        migrations.RemoveField(
            model_name='orderpayment',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderpayment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='order_payment',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='polymorphic_ctype',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='payment',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='polymorphic_ctype',
        ),
        migrations.DeleteModel(
            name='OrderPayment',
        ),
        migrations.DeleteModel(
            name='OrderPaymentAction',
        ),
    ]
