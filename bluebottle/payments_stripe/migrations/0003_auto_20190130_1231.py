# Generated by Django 1.10.8 on 2019-01-30 11:31

from django.db import migrations, models



class Migration(migrations.Migration):

    dependencies = [
        ('payments_stripe', '0002_stripepayment_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='stripepayment',
            name='payout_amount',
            field=models.IntegerField(help_text='Payment amount in smallest units (e.g. cents).', null=True),
        ),
        migrations.AddField(
            model_name='stripepayment',
            name='payout_currency',
            field=models.CharField(default=b'EUR', max_length=3),
        ),
    ]
