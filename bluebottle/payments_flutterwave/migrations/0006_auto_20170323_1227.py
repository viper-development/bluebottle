# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-23 11:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments_flutterwave', '0005_auto_20170210_1058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flutterwavepayment',
            name='bvn',
        ),
        migrations.RemoveField(
            model_name='flutterwavepayment',
            name='cvv',
        ),
        migrations.RemoveField(
            model_name='flutterwavepayment',
            name='expiry_month',
        ),
        migrations.RemoveField(
            model_name='flutterwavepayment',
            name='expiry_year',
        ),
        migrations.RemoveField(
            model_name='flutterwavepayment',
            name='pin',
        ),
    ]