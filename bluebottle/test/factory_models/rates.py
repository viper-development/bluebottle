import factory
from djmoney.contrib.exchange.models import Rate, ExchangeBackend


class RateSourceFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = ExchangeBackend

    name = 'openexchange.org'
    base_currency = 'USD'


class RateFactory(factory.DjangoModelFactory):
    class Meta(object):
        model = Rate

    source = factory.SubFactory(RateSourceFactory)
