from django.shortcuts import render
from django.urls import path
from . import views



app_name = "contact_form"

urlpatterns = [
    path("", views.contact_view, name="form"),
    path("success/", lambda r: render(r, "contact_form/success.html"), name="success"),
]
