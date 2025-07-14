# from django.urls import path
# from .api_views import PropertyListAPIView, PropertyDetailAPIView, OfficeListAPIView, BillboardListAPIView

# urlpatterns = [
#     path('offices/', OfficeListAPIView.as_view(), name='office-list'),
#     path('billboards/<uuid:public_id>/', PropertyDetailAPIView.as_view(), name='billboard-detail'),  # ⬅️ выше!
#     path('billboards/', BillboardListAPIView.as_view(), name='billboard-list'),
#     path('<uuid:public_id>/', PropertyDetailAPIView.as_view(), name='property-detail'),
#     path('', PropertyListAPIView.as_view(), name='property-list'),
# ]
# #comment 
from django.urls import path
from .views import PropertyListView, PropertyDetailView


urlpatterns = [
    path('offices/', PropertyListView.as_view(), name='property_list'),
    path('offices/<uuid:public_id>/', PropertyDetailView.as_view(), name='property_detail'),

]