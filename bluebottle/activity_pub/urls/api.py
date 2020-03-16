from django.conf.urls import url

from bluebottle.activity_pub.views import (
    RelatedPlatformView,
)

urlpatterns = [
    url(
        r'^request$',
        RelatedPlatformView.as_view(),
        name='related-platform-view'),
]
