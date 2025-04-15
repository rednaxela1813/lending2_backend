from django.urls import path
from .api_views import PropertyListAPIView, PropertyDetailAPIView



urlpatterns = [
    path('', PropertyListAPIView.as_view(), name='property-list'),
    path('<uuid:public_id>/', PropertyDetailAPIView.as_view(), name='property-detail'),
]
