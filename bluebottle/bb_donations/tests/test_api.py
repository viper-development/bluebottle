import json
from mock import patch

from django.test import TestCase

from bluebottle.bb_orders.views import ManageOrderDetail
from django.core.urlresolvers import reverse
from bluebottle.bb_orders.tests.test_api import OrderApiTestCase
from bluebottle.test.factory_models.accounts import BlueBottleUserFactory
from bluebottle.test.factory_models.projects import ProjectFactory
from bluebottle.test.factory_models.orders import OrderFactory
from bluebottle.test.factory_models.donations import DonationFactory
from bluebottle.utils.model_dispatcher import get_order_model, get_model_class
from bluebottle.test.factory_models.fundraisers import FundRaiserFactory
from bluebottle.test.utils import InitProjectDataMixin

from django.core.urlresolvers import reverse
from bluebottle.utils.utils import StatusDefinition

from rest_framework import status

ORDER_MODEL = get_order_model()
DONATION_MODEL = get_model_class("DONATIONS_DONATION_MODEL")


class DonationApiTestCase(InitProjectDataMixin, TestCase):

    def setUp(self):
        self.user1 = BlueBottleUserFactory.create()
        self.user1_token = "JWT {0}".format(self.user1.get_jwt_token())

        self.init_projects()
        self.project1 = ProjectFactory.create(amount_asked=5000)
        self.project1.set_status('campaign')

        self.project2 = ProjectFactory.create(amount_asked=3750)
        self.project2.set_status('campaign')

        self.manage_order_list_url = reverse('manage-order-list')
        self.manage_donation_list_url = reverse('manage-donation-list')

        self.user = BlueBottleUserFactory.create()
        self.user_token = "JWT {0}".format(self.user.get_jwt_token())

        self.user2 = BlueBottleUserFactory.create()
        self.user_token2 = "JWT {0}".format(self.user2.get_jwt_token())

        self.project = ProjectFactory.create()
        self.order = OrderFactory.create(user=self.user)


# Mock the ManageOrderDetail check_status_psp function which will request status_check at PSP
@patch.object(ManageOrderDetail, 'check_status_psp')
class TestDonationPermissions(DonationApiTestCase):

    def test_user_is_order_owner(self):
        """ Test that a user that is owner of the order can post a new donation """
        donation1 = {
            "project": self.project.slug,
            "order": self.order.id,
            "amount": 35
        }
        self.assertEqual(DONATION_MODEL.objects.count(), 0)
        response = self.client.post(reverse('manage-donation-list'), donation1, HTTP_AUTHORIZATION=self.user_token)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DONATION_MODEL.objects.count(), 1)

    def test_user_is_not_order_owner(self):
        """ Test that a user who is not owner of an order cannot create a new donation """

        donation1 = {
            "project": self.project.slug,
            "order": self.order.id,
            "amount": 35
        }

        self.assertEqual(DONATION_MODEL.objects.count(), 0)
        response = self.client.post(reverse('manage-donation-list'), donation1, HTTP_AUTHORIZATION=self.user_token2)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(DONATION_MODEL.objects.count(), 0)

    def test_order_status_not_new(self):
        """ Test that a non-new order status produces a forbidden response """

        order = OrderFactory.create(user=self.user, status=StatusDefinition.SUCCESS)

        donation1 = {
            "project": self.project.slug,
            "order": order.id,
            "amount": 35
        }

        self.assertEqual(DONATION_MODEL.objects.count(), 0)
        response = self.client.post(reverse('manage-donation-list'), donation1, HTTP_AUTHORIZATION=self.user_token)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(DONATION_MODEL.objects.count(), 0)

    def test_order_status_new(self):
        """ Test that a new order status produces a 201 created response """

        order = OrderFactory.create(user=self.user, status=StatusDefinition.CREATED)

        donation1 = {
            "project": self.project.slug,
            "order": order.id,
            "amount": 35
        }

        self.assertEqual(DONATION_MODEL.objects.count(), 0)
        response = self.client.post(reverse('manage-donation-list'), donation1, HTTP_AUTHORIZATION=self.user_token)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DONATION_MODEL.objects.count(), 1)

    def test_donation_update_not_same_owner(self):
        """ Test that an update to a donation where the user is not the owner produces a 403"""

        donation = DonationFactory(order=self.order, amount=35)

        updated_donation = {
            "project": self.project.slug,
            "order": self.order.id,
            "amount": 50
        }

        self.assertEqual(DONATION_MODEL.objects.count(), 1)
        response = self.client.put(reverse('manage-donation-detail',
                                   kwargs={'pk': donation.id}),
                                   json.dumps(updated_donation),
                                   'application/json',
                                   HTTP_AUTHORIZATION=self.user_token2)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(DONATION_MODEL.objects.count(), 1)

    def test_donation_update_same_owner(self):
        """ Test that an update to a donation where the user is the owner produces a 200 OK"""

        donation = DonationFactory(order=self.order, amount=35)

        updated_donation = {
            "project": self.project.slug,
            "order": self.order.id,
            "amount": 50
        }

        self.assertEqual(DONATION_MODEL.objects.count(), 1)
        response = self.client.put(reverse('manage-donation-detail',
                                   kwargs={'pk': donation.id}),
                                   json.dumps(updated_donation),
                                   'application/json',
                                   HTTP_AUTHORIZATION=self.user_token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DONATION_MODEL.objects.count(), 1)

    def test_donation_update_order_not_new(self):
        """ Test that an update to a donation where the order does not have status CREATED produces 403 FORBIDDEN"""

        order = OrderFactory.create(user=self.user, status=StatusDefinition.SUCCESS)

        donation = DonationFactory(order=order, amount=35)

        updated_donation = {
            "project": self.project.slug,
            "order": order.id,
            "amount": 50
        }

        self.assertEqual(DONATION_MODEL.objects.count(), 1)
        response = self.client.put(reverse('manage-donation-detail',
                                   kwargs={'pk': donation.id}),
                                   json.dumps(updated_donation),
                                   'application/json',
                                   HTTP_AUTHORIZATION=self.user_token)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(DONATION_MODEL.objects.count(), 1)

    def test_donation_update_order_new(self):
        """ Test that an update to a donation where the order does has status CREATED produces 200 OK response"""

        order = OrderFactory.create(user=self.user, status=StatusDefinition.CREATED)

        donation = DonationFactory(order=order, amount=35)

        updated_donation = {
            "project": self.project.slug,
            "order": order.id,
            "amount": 50
        }

        self.assertEqual(DONATION_MODEL.objects.count(), 1)
        response = self.client.put(reverse('manage-donation-detail',
                                   kwargs={'pk': donation.id}),
                                   json.dumps(updated_donation),
                                   'application/json',
                                   HTTP_AUTHORIZATION=self.user_token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DONATION_MODEL.objects.count(), 1)


class TestCreateDonation(DonationApiTestCase):

    def test_create_single_donation(self, mock_check_status_psp):
        """
        Test donation in the current donation flow where we have just one donation that can't be deleted.
        """

        # Create an order
        response = self.client.post(self.manage_order_list_url, {}, HTTP_AUTHORIZATION=self.user1_token)
        order_id = response.data['id']

        fundraiser = FundRaiserFactory.create(amount=100)

        donation1 = {
            "fundraiser": fundraiser.pk,
            "project": fundraiser.project.slug,
            "order": order_id,
            "amount": 50
        }

        response = self.client.post(self.manage_donation_list_url, donation1, HTTP_AUTHORIZATION=self.user1_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'created')
        donation_id = response.data['id']



        # Check that the order total is equal to the donation amount
        order_url = "{0}{1}".format(self.manage_order_list_url, order_id)
        response = self.client.get(order_url, HTTP_AUTHORIZATION=self.user1_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total'], 50)

    def test_create_fundraiser_donation(self, mock_check_status_psp):
        """
        Test donation in the current donation flow where we have just one donation that can't be deleted.
        """

        # Create an order
        response = self.client.post(self.manage_order_list_url, {}, HTTP_AUTHORIZATION=self.user1_token)
        order_id = response.data['id']

        donation1 = {
            "project": self.project1.slug,
            "order": order_id,
            "amount": 35
        }

        response = self.client.post(self.manage_donation_list_url, donation1, HTTP_AUTHORIZATION=self.user1_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'created')
        donation_id = response.data['id']

        # Check that the order total is equal to the donation amount
        order_url = "{0}{1}".format(self.manage_order_list_url, order_id)
        response = self.client.get(order_url, HTTP_AUTHORIZATION=self.user1_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total'], 35)

    def test_crud_multiple_donations(self, mock_check_status_psp):
        """
        Test more advanced modifications to donations and orders that aren't currently supported by our
        front-en but
        """

        # Create an order
        response = self.client.post(self.manage_order_list_url, {}, HTTP_AUTHORIZATION=self.user1_token)
        order_id = response.data['id']

        donation1 = {
            "project": self.project1.slug,
            "order": order_id,
            "amount": 35
        }

        response = self.client.post(self.manage_donation_list_url, donation1, HTTP_AUTHORIZATION=self.user1_token)
        donation_id = response.data['id']

        # Check that the order total is equal to the donation amount
        order_url = "{0}{1}".format(self.manage_order_list_url, order_id)
        response = self.client.get(order_url, HTTP_AUTHORIZATION=self.user1_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total'], 35)

        # Check that this user can change the amount
        donation_url = "{0}{1}".format(self.manage_donation_list_url, donation_id)
        donation1['amount'] = 50
        response = self.client.put(donation_url, json.dumps(donation1), 'application/json', HTTP_AUTHORIZATION=self.user1_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the order total is equal to the increased donation amount
        order_url = "{0}{1}".format(self.manage_order_list_url, order_id)
        response = self.client.get(order_url, HTTP_AUTHORIZATION=self.user1_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total'], 50)

        # Add another donation
        donation2 = {
            "project": self.project2.slug,
            "order": order_id,
            "amount": 47
        }
        response = self.client.post(self.manage_donation_list_url, donation2, HTTP_AUTHORIZATION=self.user1_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'created')

        # Check that the order total is equal to the two donations
        order_url = "{0}{1}".format(self.manage_order_list_url, order_id)
        response = self.client.get(order_url, HTTP_AUTHORIZATION=self.user1_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['donations']), 2)
        self.assertEqual(response.data['total'], 97)

        # remove the first donation
        response = self.client.delete(donation_url, content_type='application/json', HTTP_AUTHORIZATION=self.user1_token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check that the order total is equal to second donation
        order_url = "{0}{1}".format(self.manage_order_list_url, order_id)
        response = self.client.get(order_url, HTTP_AUTHORIZATION=self.user1_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['donations']), 1)
        self.assertEqual(response.data['total'], 47)

        # Set order to status 'locked'
        order = ORDER_MODEL.objects.get(id=order_id)
        order.locked()

        donation3 = {
            "project": self.project1.slug,
            "order": order_id,
            "amount": 70
        }

        # Should not be able to add more donations to this order now.
        response = self.client.post(self.manage_donation_list_url, donation3, HTTP_AUTHORIZATION=self.user1_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Check that this user can't change the amount of an donation
        donation1['amount'] = 5
        response = self.client.put(donation_url, json.dumps(donation1), content_type='application/json', HTTP_AUTHORIZATION=self.user1_token)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestDonationCreate(DonationApiTestCase):

    def test_create_anonymous_donation(self):
        donation_url = reverse('manage-donation-list')

        # create a new anonymous donation
        response = self.client.post(donation_url, {'order': self.order.pk, 'project': self.project.slug, 'amount': 50, 'anonymous': True}, HTTP_AUTHORIZATION=self.user_token)

        self.assertEqual(response.status_code, 201)

        # retrieve the donation just created
        donation_id = response.data['id']
        donation_url = reverse('manage-donation-detail', kwargs={'pk': donation_id})
        response = self.client.get(donation_url, HTTP_AUTHORIZATION=self.user_token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the anonymous is set to True
        self.assertEqual(True, response.data['anonymous'])

        # Check that user is shown in private API
        self.assertEqual(self.order.user.id, response.data['user'])

        # Set the order to success
        self.order.locked()
        self.order.succeeded()

        # retrieve the donation through public API
        donation_url = reverse('donation-detail', kwargs={'pk': donation_id})
        response = self.client.get(donation_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that user is NOT shown in public API
        self.assertEqual(None, response.data['user'])
