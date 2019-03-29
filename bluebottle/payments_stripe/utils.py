from django.core.exceptions import ImproperlyConfigured
from bluebottle.clients import properties


def get_webhook_secret(key='webhook_secret'):
    for account in properties.MERCHANT_ACCOUNTS:
        if account['merchant'] == 'stripe':
            return account[key]

    raise ImproperlyConfigured('No merchant account for stripe')


def get_secret_key():
    for account in properties.MERCHANT_ACCOUNTS:
        if account['merchant'] == 'stripe':
            return account['secret_key']

    raise ImproperlyConfigured('No merchant account for stripe')


def get_stripe_settings():
    for account in properties.MERCHANT_ACCOUNTS:
        if account['merchant'] == 'stripe':
            return {'publishable_key': account['publishable_key']}