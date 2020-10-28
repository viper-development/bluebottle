# Generated by Django 1.11.15 on 2019-09-18 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('funding', '0031_plainpayoutaccount'),
        ('funding_vitepay', '0005_vitepaypayoutaccount'),
    ]

    operations = [
        migrations.CreateModel(
            name='VitepayBankAccount',
            fields=[
                ('bankaccount_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='funding.BankAccount')),
                ('account_name', models.CharField(max_length=40)),
            ],
            options={
                'abstract': False,
            },
            bases=('funding.bankaccount',),
        ),
        migrations.RemoveField(
            model_name='vitepaypayoutaccount',
            name='payoutaccount_ptr',
        ),
        migrations.DeleteModel(
            name='VitepayPayoutAccount',
        ),
    ]
