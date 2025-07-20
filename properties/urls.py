from django.urls import path
from .views import  PropertyListView, PropertyDetailView, AddressListView, BillboardListView


urlpatterns = [
    path('offices/', PropertyListView.as_view(), name='property_list'),
    path('offices/<uuid:public_id>/', PropertyDetailView.as_view(), name='office_detail'),

    path('addresses/', AddressListView.as_view(), name='address_list'),
    path('addresses/<uuid:public_id>/', PropertyDetailView.as_view(), name='address_detail'),

    path('billboards/', BillboardListView.as_view(), name='billboard_list'),
    path('billboards/<uuid:public_id>/', PropertyDetailView.as_view(), name='billboard_detail'),
]

