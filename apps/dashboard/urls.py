from django.urls import path
from .views import (
    DashboardHome,
    TextList, TextCreate, TextUpdate, TextDelete,
    ImageList, ImageCreate, ImageUpdate, ImageDelete,
)

app_name = "dashboard"

urlpatterns = [
    path("", DashboardHome.as_view(), name="home"),

    # текстовый контент
    path("texts/", TextList.as_view(), name="text_list"),
    path("texts/new/", TextCreate.as_view(), name="text_create"),
    path("texts/<int:pk>/edit/", TextUpdate.as_view(), name="text_update"),
    path("texts/<int:pk>/delete/", TextDelete.as_view(), name="text_delete"),

    # изображения
    path("images/", ImageList.as_view(), name="image_list"),
    path("images/new/", ImageCreate.as_view(), name="image_create"),
    path("images/<int:pk>/edit/", ImageUpdate.as_view(), name="image_update"),
    path("images/<int:pk>/delete/", ImageDelete.as_view(), name="image_delete"),
]
