# apps/hotdeal/urls.py
from django.urls import path
from apps.hotdeal import views

app_name = "hotdeal"                             

urlpatterns = [
    path("partial/<uuid:public_id>/", views.hotdeal_partial, name="partial"),
   # path("<uuid:public_id>/", HotDealDetailView.as_view(), name="detail"),
    path("partial/empty/", views.hotdeal_partial_empty, name="partial_empty"),
         
]
