from django.views.generic import View
from django.http import HttpResponse

from rest_framework_json_api.views import AutoPrefetchMixin


from bluebottle.funding.views import PaymentList
from bluebottle.funding_stripe import stripe
from bluebottle.funding_stripe.models import StripePayment, StripeKYCCheck
from bluebottle.funding_stripe.serializers import StripePaymentSerializer, StripeKYCCheckSerializer
from bluebottle.utils.permissions import IsOwner
from bluebottle.utils.views import (
    RetrieveUpdateAPIView, JsonApiViewMixin, CreateAPIView,
)


class StripePaymentList(PaymentList):
    queryset = StripePayment.objects.all()
    serializer_class = StripePaymentSerializer


class StripeKYCCheckList(JsonApiViewMixin, AutoPrefetchMixin, CreateAPIView):
    queryset = StripeKYCCheck.objects.all()
    serializer_class = StripeKYCCheckSerializer

    prefetch_for_includes = {
        'user': ['user'],
    }

    permission_classes = (IsOwner, )

    def perform_create(self, serializer):
        token = serializer.validated_data.pop('token')
        serializer.save(owner=self.request.user)
        serializer.instance.update(token)


class StripeKYCCheckDetails(JsonApiViewMixin, AutoPrefetchMixin, RetrieveUpdateAPIView):
    queryset = StripeKYCCheck.objects.all()
    serializer_class = StripeKYCCheckSerializer

    prefetch_for_includes = {
        'user': ['user'],
    }

    permission_classes = (IsOwner, )


class WebHookView(View):
    def post(self, request, **kwargs):

        payload = request.body
        signature_header = request.META['HTTP_STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(
                payload, signature_header, stripe.webhook_secret
            )
        except stripe.error.SignatureVerificationError:
            # Invalid signature
            return HttpResponse('Signature failed to verify', status=400)

        try:
            if event.type == 'payment_intent.succeeded':
                payment = self.get_payment(event.data.object.id)
                payment.transitions.succeed()
                payment.save()

                return HttpResponse('Updated payment')

            if event.type == 'payment_intent.payment_failed':
                payment = self.get_payment(event.data.object.id)
                payment.transitions.fail()
                payment.save()

                return HttpResponse('Updated payment')

            if event.type == 'charge.refunded':
                payment = self.get_payment(event.data.object.payment_intent)
                payment.transitions.refund()
                payment.save()

                return HttpResponse('Updated payment')

        except StripePayment.DoesNotExist:
            return HttpResponse('Payment not found', status=400)

    def get_payment(self, intent_id):
        return StripePayment.objects.get(intent_id=intent_id)
