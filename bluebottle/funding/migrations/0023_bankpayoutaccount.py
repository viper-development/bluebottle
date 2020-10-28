# Generated by Django 1.11.15 on 2019-08-26 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('funding', '0022_auto_20190804_1022'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankPayoutAccount',
            fields=[
                ('payoutaccount_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='funding.PayoutAccount')),
                ('account_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='bank account number')),
                ('account_holder_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='account holder name')),
                ('account_holder_address', models.CharField(blank=True, max_length=500, null=True, verbose_name='account holder address')),
                ('account_bank_country', models.CharField(blank=True, max_length=100, null=True, verbose_name='bank country')),
                ('account_details', models.CharField(blank=True, max_length=500, null=True, verbose_name='account details')),
            ],
            options={
                'abstract': False,
            },
            bases=('funding.payoutaccount',),
        ),
    ]
