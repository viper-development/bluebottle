import json
import logging

from django.http import JsonResponse
from django.views.generic.base import View

from bluebottle.payments.models import OrderPayment
from bluebottle.payments.services import PaymentService

logger = logging.getLogger(__name__)


class PaymentUpdateView(View):

    permanent = False
    query_string = True
    pattern_name = 'cellulant-update-payment'
    """
    {
      "MSISDN": "254724778819",
      "amountPaid": 750,
      "requestStatusCode": 178,
      "serviceCode": "GOOSBX8683",
      "requestStatusDescription": "Request fully paid",
      "payments": [
        {
          "MSISDN": 254724778819,
          "amountPaid": 750,
          "cpgTransactionID": "10364561",
          "serviceCode": "GOOSBX8683",
          "payerTransactionID": "dev-test-1535603160",
          "accountNumber": "123456",
          "currencyCode": "KES",
          "customerName": "Customer",
          "payerClientCode": "AIRTELKE",
          "datePaymentReceived": "2018-08-30 10:26:14.0"
        }
      ],
      "merchantTransactionID": "78874",
      "requestDate": "2018-08-30 07:08:04.0",
      "checkoutRequestID": 204026,
      "requestAmount": "750.00",
      "accountNumber": "123456",
      "currencyCode": "KES"
    }
    """
    def post(self, request):
        payload = json.loads(request.body)
        order_id = payload['merchantTransactionID']
        order_payment = OrderPayment.objects.get(id=order_id)
        service = PaymentService(order_payment)
        service.check_payment_status()
        return JsonResponse({'status': 'success'})
