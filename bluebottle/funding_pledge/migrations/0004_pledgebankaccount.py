# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-10-22 09:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('funding', '0039_auto_20191022_1105'),
        ('geo', '0014_auto_20191022_1105'),
        ('funding_pledge', '0003_auto_20191002_0903'),
    ]

    operations = [
        migrations.CreateModel(
            name='PledgeBankAccount',
            fields=[
                ('bankaccount_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='funding.BankAccount')),
                ('account_holder_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Account holder name')),
                ('account_holder_address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Account holder address')),
                ('account_holder_postal_code', models.CharField(blank=True, max_length=20, null=True, verbose_name='Account holder postal code')),
                ('account_holder_city', models.CharField(blank=True, max_length=255, null=True, verbose_name='Account holder city')),
                ('account_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='Account number')),
                ('account_details', models.CharField(blank=True, max_length=500, null=True, verbose_name='Account details')),
                ('account_bank_country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pledge_account_bank_country', to='geo.Country', verbose_name='Account bank country')),
                ('account_holder_country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pledge_account_holder_country', to='geo.Country', verbose_name='Account holder country')),
            ],
            options={
                'verbose_name': 'Pledge bank account',
                'verbose_name_plural': 'Pledge bank accounts',
            },
            bases=('funding.bankaccount',),
        ),
    ]
