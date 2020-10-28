import factory

from bluebottle.follow.models import Follow
from bluebottle.initiatives.tests.factories import InitiativeFactory
from bluebottle.events.tests.factories import EventFactory
from bluebottle.funding.tests.factories import FundingFactory
from bluebottle.test.factory_models.accounts import BlueBottleUserFactory


class InitiativeFollowFactory(factory.DjangoModelFactory):
    class Meta:
        model = Follow
    user = factory.SubFactory(BlueBottleUserFactory)
    instance = factory.SubFactory(InitiativeFactory)


class EventFollowFactory(factory.DjangoModelFactory):
    class Meta:
        model = Follow
    user = factory.SubFactory(BlueBottleUserFactory)
    instance = factory.SubFactory(EventFactory)


class FundingFollowFactory(factory.DjangoModelFactory):
    class Meta:
        model = Follow
    user = factory.SubFactory(BlueBottleUserFactory)
    instance = factory.SubFactory(FundingFactory)
