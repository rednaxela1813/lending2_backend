from django.urls import path
from .api_views import PropertyListAPIView, PropertyDetailAPIView, OfficeListAPIView, BillboardListAPIView

urlpatterns = [
    path('offices/', OfficeListAPIView.as_view(), name='office-list'), 
    path('', PropertyListAPIView.as_view(), name='property-list'),
    path('<uuid:public_id>/', PropertyDetailAPIView.as_view(), name='property-detail'),
    path('billboards/', BillboardListAPIView.as_view(), name='billboard-list'),
    path('billboards/<uuid:public_id>/', PropertyDetailAPIView.as_view(), name='billboard-detail'),

]
