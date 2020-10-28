# Generated by Django 1.11.15 on 2020-01-24 09:32

import bluebottle.utils.fields
from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('funding', '0048_add_permissions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payout',
            options={'verbose_name': 'payout', 'verbose_name_plural': 'payouts'},
        ),
        migrations.AlterModelOptions(
            name='plainpayoutaccount',
            options={'verbose_name': 'Without payment account', 'verbose_name_plural': 'Without payment accounts'},
        ),
        migrations.AddField(
            model_name='donation',
            name='payout_amount',
            field=bluebottle.utils.fields.MoneyField(currency_choices=[(b'EUR', b'Euro')], decimal_places=2, default=Decimal('0.0'), default_currency=b'EUR', max_digits=12),
        ),
        migrations.AddField(
            model_name='donation',
            name='payout_amount_currency',
            field=djmoney.models.fields.CurrencyField(choices=[(b'EUR', b'Euro')], default=b'EUR', editable=False, max_length=3),
        ),
        migrations.AlterField(
            model_name='donation',
            name='fundraiser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='donations', to='funding.Fundraiser'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='name',
            field=models.CharField(blank=True, help_text='Override donor name / Name for guest donation', max_length=200, null=True, verbose_name='Fake name'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='reward',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='donations', to='funding.Reward'),
        ),
        migrations.AlterField(
            model_name='funding',
            name='deadline',
            field=models.DateTimeField(blank=True, help_text='If you enter a deadline, leave the duration field empty.', null=True, verbose_name='deadline'),
        ),
        migrations.AlterField(
            model_name='funding',
            name='duration',
            field=models.PositiveIntegerField(blank=True, help_text='If you enter a duration, leave the deadline field empty.', null=True, verbose_name='duration'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='updated',
            field=models.DateTimeField(),
        ),
    ]
