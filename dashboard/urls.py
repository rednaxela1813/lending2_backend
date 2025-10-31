from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    # домашняя панель
    path("", views.DashboardHome.as_view(), name="home"),

    # тексты
    path("texts/", views.TextList.as_view(), name="text_list"),
    path("texts/create/", views.TextCreate.as_view(), name="text_create"),
    path("texts/<int:pk>/edit/", views.TextUpdate.as_view(), name="text_update"),
    path("texts/<int:pk>/delete/", views.TextDelete.as_view(), name="text_delete"),

    # изображения
    path("images/", views.ImageList.as_view(), name="image_list"),
    path("images/create/", views.ImageCreate.as_view(), name="image_create"),
    path("images/<int:pk>/edit/", views.ImageUpdate.as_view(), name="image_update"),
    path("images/<int:pk>/delete/", views.ImageDelete.as_view(), name="image_delete"),
]
