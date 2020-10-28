# Generated by Django 1.10.8 on 2018-04-04 11:00

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('payments', '0005_auto_20170919_1621'),
    ]

    operations = [
        migrations.CreateModel(
            name='BeyonicPayment',
            fields=[
                ('payment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='payments.Payment')),
                ('amount', models.CharField(blank=True, help_text=b'Amount', max_length=200, null=True)),
                ('currency', models.CharField(blank=True, default=b'USD', help_text=b'Transaction currency', max_length=200, null=True)),
                ('mobile', models.CharField(blank=True, help_text=b'Mobile Number', max_length=200, null=True)),
                ('description', models.CharField(blank=True, help_text=b'Description', max_length=200, null=True)),
                ('metadata', django_extensions.db.fields.json.JSONField(blank=True, default=dict, help_text=b'Metadata', max_length=100, null=True)),
                ('transaction_reference', models.CharField(blank=True, help_text=b'Transaction ID', max_length=200, null=True)),
                ('response', models.TextField(blank=True, help_text='Response from Beyonic', null=True)),
                ('update_response', models.TextField(blank=True, help_text='Result from Beyonic (status update)', null=True)),
            ],
            options={
                'ordering': ('-created', '-updated'),
                'verbose_name': 'Beyonic Payment',
                'verbose_name_plural': 'Beyonic Payments',
            },
            bases=('payments.payment',),
        ),
    ]
