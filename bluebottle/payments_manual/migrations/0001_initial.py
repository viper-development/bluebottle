# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-23 13:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('payments', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManualPayment',
            fields=[
                ('payment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='payments.Payment')),
                ('amount', models.DecimalField(decimal_places=2, editable=False, max_digits=15, verbose_name='amount')),
                ('bank_transaction', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='accounting.BankTransaction')),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'manual payment',
                'verbose_name_plural': 'manual payments',
            },
            bases=('payments.payment',),
        ),
    ]
