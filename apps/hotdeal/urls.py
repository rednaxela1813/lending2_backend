# apps/hotdeal/urls.py
from django.urls import path
from .views import hotdeal_partial, HotDealDetailView

app_name = "hotdeal"                             

urlpatterns = [
    path("partial/<uuid:public_id>/", hotdeal_partial, name="partial"),
    path("<uuid:public_id>/", HotDealDetailView.as_view(), name="detail"),
         
]
