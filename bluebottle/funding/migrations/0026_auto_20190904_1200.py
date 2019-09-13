# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-09-04 10:00
from __future__ import unicode_literals

from django.db import migrations, connection

from bluebottle.clients import properties


def migrate_payment_providers(apps, schema_editor):

    PledgePaymentProvider = apps.get_model('funding_pledge', 'PledgePaymentProvider')
    StripePaymentProvider = apps.get_model('funding_stripe', 'StripePaymentProvider')
    FlutterwavePaymentProvider = apps.get_model('funding_flutterwave', 'FlutterwavePaymentProvider')
    VitepayPaymentProvider = apps.get_model('funding_vitepay', 'VitepayPaymentProvider')
    LipishaPaymentProvider = apps.get_model('funding_lipisha', 'LipishaPaymentProvider')

    Client = apps.get_model('clients', 'Client')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    tenant = Client.objects.get(schema_name=connection.tenant.schema_name)
    properties.set_tenant(tenant)

    for provider in properties.MERCHANT_ACCOUNTS:
        if provider['merchant'] == 'stripe':
            content_type = ContentType.objects.get_for_model(StripePaymentProvider)
            stripe = StripePaymentProvider.objects.create(
                polymorphic_ctype=content_type,
            )
            for payment_methods in properties.PAYMENT_METHODS:
                if payment_methods['id'] == 'stripe-creditcard':
                    stripe.credit_card = True
                elif payment_methods['id'] == 'stripe-ideal':
                    stripe.ideal = True
                elif payment_methods['id'] == 'stripe-directdebit':
                    stripe.direct_debit = True
                elif payment_methods['id'] == 'stripe-bancontact':
                    stripe.bancontact = True
            stripe.save()
        elif provider['merchant'] == 'vitepay':
            content_type = ContentType.objects.get_for_model(VitepayPaymentProvider)
            VitepayPaymentProvider.objects.create(
                polymorphic_ctype=content_type,
                api_secret=provider['api_secret'],
                api_key=provider['api_key'],
                api_url=provider['api_url'],
                prefix='ne'
            )
        elif provider['merchant'] == 'lipisha':
            content_type = ContentType.objects.get_for_model(LipishaPaymentProvider)
            LipishaPaymentProvider.objects.create(
                polymorphic_ctype=content_type,
                api_key=provider['api_key'],
                api_signature=provider['api_signature'],
                paybill=provider['business_number'],
                prefix='ne'
            )
        elif provider['merchant'] == 'flutterwave':
            content_type = ContentType.objects.get_for_model(FlutterwavePaymentProvider)
            FlutterwavePaymentProvider.objects.create(
                polymorphic_ctype=content_type,
                pub_key=provider['pub_key'],
                sec_key=provider['sec_key'],
                prefix='ne'
            )
        elif provider['merchant'] == 'pledge':
            content_type = ContentType.objects.get_for_model(PledgePaymentProvider)
            PledgePaymentProvider.objects.create(
                polymorphic_ctype=content_type,
            )

def wipe_payment_providers(apps, schema_editor):

    PaymentProvider = apps.get_model('funding', 'PaymentProvider')
    PaymentProvider.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('funding', '0025_auto_20190904_1154'),
        ('funding_pledge', '0002_pledgepaymentprovider'),
        ('funding_lipisha', '0003_lipishapayoutaccount'),
        ('funding_flutterwave', '0003_flutterwavepayoutaccount'),
        ('funding_stripe', '0011_merge_20190729_1449'),
        ('funding_vitepay', '0004_auto_20190715_0739'),
    ]

    operations = [
        migrations.RunPython(migrate_payment_providers, wipe_payment_providers)
    ]
