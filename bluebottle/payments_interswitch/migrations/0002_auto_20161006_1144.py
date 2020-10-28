# Generated by Django 1.9.6 on 2016-10-06 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments_interswitch', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interswitchpayment',
            name='amount',
            field=models.CharField(blank=True, help_text='Transaction amount in small (kobo or cents)', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='interswitchpayment',
            name='cust_id_desc',
            field=models.CharField(blank=True, help_text='Customer Identification Number description.', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='interswitchpayment',
            name='cust_name_desc',
            field=models.CharField(blank=True, help_text='Customer Name Description.', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='interswitchpayment',
            name='hash',
            field=models.CharField(blank=True, help_text='A Hashed value of selected combined parameters.', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='interswitchpayment',
            name='local_date_time',
            field=models.CharField(blank=True, help_text='Local Transaction Date time', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='interswitchpayment',
            name='site_name',
            field=models.CharField(blank=True, help_text='Internet site name of the web site', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='interswitchpayment',
            name='site_redirect_url',
            field=models.CharField(blank=True, help_text='URL the user is to be redirected to after payment.', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='interswitchpayment',
            name='txn_ref',
            field=models.CharField(blank=True, help_text='Transaction Reference Number.', max_length=200, null=True),
        ),
    ]
