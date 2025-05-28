from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import LegalAddressOrder
from .serializers import LegalAddressOrderSerializer
from rest_framework.response import Response


class LegalAddressOrderCreateAPIView(generics.CreateAPIView):
    """
    API view to create a legal address order.
    """
    queryset = LegalAddressOrder.objects.all()
    serializer_class = LegalAddressOrderSerializer