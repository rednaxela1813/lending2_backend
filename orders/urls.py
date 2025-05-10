from django.urls import path
from .api_views import LegalAddressOrderCreateAPIView


urlpatterns = [
    path('legal-address/', LegalAddressOrderCreateAPIView.as_view(), name='legal-address-order'),
]
