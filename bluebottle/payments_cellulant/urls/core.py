from django.conf.urls import url

from bluebottle.payments_cellulant.views import PaymentUpdateView


urlpatterns = [
    url(r'^update/$',
        PaymentUpdateView.as_view(),
        name='cellulant-update-payment'),
]
