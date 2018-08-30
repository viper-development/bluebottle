# coding=utf-8
import json
import logging

from moneyed.classes import Money
from mula.adpaters import MulaAdapter
from mula.exceptions import MulaPaymentException

from bluebottle.payments.exception import PaymentException
from bluebottle.payments.adapters import BasePaymentAdapter


from .models import CellulantPayment

logger = logging.getLogger()


class CellulantPaymentAdapter(BasePaymentAdapter):
    card_data = {}

    def __init__(self, order_payment):
        self.order_payment = order_payment
        self.client = MulaAdapter(
            self.credentials['client_id'],
            self.credentials['client_secret'],
            self.credentials['service_code']
        )
        super(CellulantPaymentAdapter, self).__init__(order_payment)

    def _update_amounts(self, payment, amount, currency):
        order_payment = payment.order_payment
        order_payment.amount = Money(amount, currency)
        order_payment.save()

        donation = payment.order_payment.order.donations.first()
        donation.amount = Money(amount, currency)
        donation.save()

        payment.amount = amount
        payment.save()

    def create_payment(self):
        payment = CellulantPayment(
            order_payment=self.order_payment,
        )
        self.card_data = self.order_payment.card_data

        payment.msisdn = self.card_data['mobile']
        payment.account_number = '123456'
        payment.reference = payment.order_payment.id
        payment.amount = payment.order_payment.amount.amount
        payment.currency = 'KES'
        payment.country_code = 'KE'
        payment.callback_url = 'https://webhook.site/a9285d46-23c8-4c69-b2b2-0017ca024856'
        payment.status = 'started'
        payment.description = 'Test'
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

        # Lookup id for Mpesa USSD Push
        options = response['results']['paymentOptions']
        mpesa = [i for i in options if i['paymentModeID'] == 3][0]

        payment.payer_mode_id = mpesa['payerModeID']

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

        payment.update_response = json.dumps(response)

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

        # Later include instructions how to manually transer the money.
        # We need to know Paybill and Account number for this.
        message = "You will receive a USSD push notification shortly. " \
                  "Please confirm the payment with your PIN."

        if self.payment.status in ['settled', 'authorized']:
            return {
                'type': 'success'
            }
        else:
            return {
                'type': 'process',
                'payload': message
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

        payment.update_response = "{}\n{}".format(payment.update_response, json.dumps(response))
        payment.save()

        if not response.get('results', None):
            payment.status = 'failed'
            payment.save()
            return payment

        amount_paid = response['results']['amountPaid']
        if amount_paid > 0:
            if amount_paid != payment.amount:
                self._update_amounts(payment, amount_paid, payment.currency)
            payment.status = 'settled'
            payment.save()
