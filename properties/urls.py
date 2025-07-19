from django.urls import path
from .views import  PropertyListView, PropertyDetailView, AddressListView, BillboardListView

urlpatterns = [
    # Главная страница
   

    # Список офисов
    path('offices/', PropertyListView.as_view(), name='property_list'),

    # Детальная страница Property (любой тип: office, address, billboard)
    path('<uuid:public_id>/', PropertyDetailView.as_view(), name='property_detail'),
    path('addresses/', AddressListView.as_view(), name='address_list'),
    path('addresses/<uuid:public_id>/', PropertyDetailView.as_view(), name='property_detail'), 
    path('billboards/', BillboardListView.as_view(), name='billboard_list'),
    path('billboards/<uuid:public_id>/', PropertyDetailView.as_view(), name='property_detail'),
]
