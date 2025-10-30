from django.urls import path
from . import views

app_name = "contact_messages"

urlpatterns = [
    path("contact/submit/", views.submit, name="submit"),
    path("contact/success/", views.success, name="success"),  # простая страница «спасибо»
]
