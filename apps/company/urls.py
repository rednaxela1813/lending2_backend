from django.urls import path
from apps.company import views


app_name = "company"

urlpatterns = [
    path("about-us/", views.about_us_view, name="about_us"),
]