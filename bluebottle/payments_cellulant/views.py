import logging
from django.http import JsonResponse
from django.views.generic.base import View

from bluebottle.payments_cellulant.adapters import CellulantPaymentInterface

logger = logging.getLogger(__name__)


class PaymentUpdateView(View):

    permanent = False
    query_string = True
    pattern_name = 'cellulant-payment-initiate'

    def post(self, request):
        if request.POST['api_type'] == 'Initiate':
            if request.POST['transaction_type'] == 'Payment':
                interface = CellulantPaymentInterface()
                payment_response = interface.initiate_payment(request.POST)
                data = payment_response
                return JsonResponse(data)
            else:
                logger.error('Could not parse Cellulant Paymnent update: '
                             'Unknown transaction_type {}'.format(request.POST['transaction_type']))
        if request.POST['api_type'] == 'Acknowledge':
            interface = CellulantPaymentInterface()
            payment_response = interface.acknowledge_payment(request.POST)
            data = payment_response
            return JsonResponse(data)
        else:
            logger.error('Could not parse Cellulant Paymnent update: '
                         'Unknown api_type {}'.format(request.POST['api_type']))
