# Generated by Django 1.9.4 on 2016-05-23 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PledgeStandardPayment',
            fields=[
                ('payment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='payments.Payment')),
            ],
            options={
                'abstract': False,
            },
            bases=('payments.payment',),
        ),
    ]
