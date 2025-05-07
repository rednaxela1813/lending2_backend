from rest_framework import generics
from .models import Property
from .serializers import PropertySerializer


class PropertyListAPIView(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class PropertyDetailAPIView(generics.RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    lookup_field = 'public_id'  # Будем искать по UUID
    
    

class OfficeListAPIView(generics.ListAPIView):
    """
    API-представление, которое возвращает только объекты типа 'office'.
    """
    serializer_class = PropertySerializer

    def get_queryset(self):
        # Фильтруем Property по типу 'office'
        return Property.objects.filter(type='office')



class BillboardListAPIView(generics.ListAPIView):
    serializer_class = PropertySerializer

    def get_queryset(self):
        return Property.objects.filter(type='billboard')

