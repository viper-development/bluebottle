# coding=utf-8
import json
import logging

from bluebottle.payments.exception import PaymentException
from mula.adpaters import MulaAdapter

from bluebottle.payments.adapters import BasePaymentAdapter
from bluebottle.utils.utils import StatusDefinition
from mula.exceptions import MulaPaymentException

from .models import CellulantPayment

logger = logging.getLogger()


class CellulantPaymentAdapter(BasePaymentAdapter):
    card_data = {}

    STATUS_MAPPING = {
        'Requested': StatusDefinition.CREATED,
        'Completed': StatusDefinition.SETTLED,
        'Cancelled': StatusDefinition.CANCELLED,
        'Voided': StatusDefinition.FAILED,
        'Acknowledged': StatusDefinition.AUTHORIZED,
        'Authorized': StatusDefinition.AUTHORIZED,
        'Settled': StatusDefinition.SETTLED,
        'Reversed': StatusDefinition.REFUNDED
    }

    def __init__(self, order_payment):
        self.order_payment = order_payment
        self.client = MulaAdapter(
            self.credentials['client_id'],
            self.credentials['client_secret'],
            self.credentials['service_code']
        )
        super(CellulantPaymentAdapter, self).__init__(order_payment)

    def _get_mapped_status(self, status):
        return self.STATUS_MAPPING[status]

    def create_payment(self):
        payment = CellulantPayment(
            order_payment=self.order_payment,
        )
        self.card_data = self.order_payment.card_data

        payment.msisdn = '254800000000'
        payment.account_number = '123456'
        payment.reference = payment.order_payment.id
        payment.amount = payment.order_payment.amount.amount
        payment.currency = 'KES'
        payment.country_code = 'KE'
        payment.callback_url = 'http://cell.requestcatcher.com/'
        payment.payer_mode_id = '3'  # M-PESA push
        payment.status = 'started'
        payment.save()

        try:
            response = self.client.checkout_request(
                msisdn=payment.msisdn,
                transaction_id=payment.reference,
                account_number=payment.account_number,
                amount=payment.amount,
                currency_code=payment.currency,
                country_code=payment.country_code,
                description=payment.description,
                due_date=None,
                callback_url=payment.callback_url,
                customer_first_name='Nomen',
                customer_last_name='Nescio',
                customer_email='nomen@example.com')
        except MulaPaymentException as e:
            raise PaymentException('Could not start M-PESA transaction: {}'.format(e))
        payment.response = json.dumps(response)

        if not response.get('results', None):
            payment.status = 'failed'
            payment.save()
            return payment

        payment.remote_reference = response['results']['checkoutRequestID']

        try:
            response = self.client.charge_request(
                msisdn=payment.msisdn,
                transaction_id=payment.reference,
                checkout_request_id=payment.remote_reference,
                amount=payment.amount,
                currency_code=payment.currency,
                payer_mode_id=payment.payer_mode_id,
                language_code='en',
                country_code=payment.country_code)
        except MulaPaymentException as e:
            raise PaymentException('Could not start M-PESA transaction: {}'.format(e))

        payment.response = json.dumps(response)

        if not response.get('results', None):
            payment.status = 'failed'
            payment.save()
            return payment

        payment.status = 'started'
        payment.save()
        self.payment = payment
        return payment

    def get_authorization_action(self):

        self.check_payment_status()
        if self.payment.status in ['settled', 'authorized']:
            return {
                'type': 'success'
            }
        else:
            return {
                'type': 'pending'
            }

    def check_payment_status(self):
        payment = self.order_payment.payment

        try:
            response = self.client.request_status(
                transaction_id=payment.reference,
                checkout_request_id=payment.remote_reference
            )
        except MulaPaymentException as e:
            raise PaymentException('Could not check M-PESA transaction: {}'.format(e))

        payment.response = json.dumps(response)

        if not response.get('results', None):
            payment.status = 'failed'
            payment.save()
            return payment
