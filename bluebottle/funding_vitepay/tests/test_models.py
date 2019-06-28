from bluebottle.funding.tests.factories import FundingFactory, DonationFactory
from bluebottle.funding.transitions import PaymentTransitions
from bluebottle.funding_vitepay.models import VitepayPaymentProvider
from bluebottle.funding_vitepay.tests.factories import VitepayPaymentFactory

from bluebottle.initiatives.tests.factories import InitiativeFactory
from bluebottle.test.utils import BluebottleTestCase


class VitepayPaymentTestCase(BluebottleTestCase):
    def setUp(self):
        super(VitepayPaymentTestCase, self).setUp()
        VitepayPaymentProvider.objects.create(
            api_secret='123456789012345678901234567890123456789012345678901234567890',
            api_key='123'
        )

        self.initiative = InitiativeFactory.create()

        self.initiative.transitions.submit()
        self.initiative.transitions.approve()

        self.funding = FundingFactory.create(initiative=self.initiative)
        self.donation = DonationFactory.create(activity=self.funding)

    def test_create(self):
        payment = VitepayPaymentFactory(donation=self.donation)
        payment.save()

        self.assertEqual(payment.status, PaymentTransitions.values.new)
