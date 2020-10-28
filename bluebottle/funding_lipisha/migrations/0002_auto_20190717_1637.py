# Generated by Django 1.11.15 on 2019-07-17 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funding_lipisha', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lipishapayment',
            old_name='payment_url',
            new_name='transaction',
        ),
        migrations.AddField(
            model_name='lipishapayment',
            name='method',
            field=models.CharField(default=b'Paybill (M-Pesa)', max_length=30),
        ),
        migrations.AddField(
            model_name='lipishapaymentprovider',
            name='paybill',
            field=models.CharField(default='00000', max_length=10),
            preserve_default=False,
        ),
    ]
