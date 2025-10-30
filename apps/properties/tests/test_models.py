# apps/properties/tests/test_models.py
import pytest
from apps.properties.models.property import Property, PropertyType, PropertyImage
from django.test import override_settings
import os
from PIL import Image

pytestmark = pytest.mark.django_db


def test_create_property():
    ptype = PropertyType.objects.create(name="Offices", slug="office")
    prop = Property.objects.create(
        name="Test Property",
        type=ptype,  # <-- ВАЖНО: экземпляр PropertyType, не строка
        description="Test description",
        location="Test location",
    )
    assert prop.pk is not None
    assert prop.type == ptype
    assert prop.type.slug == "office"


@override_settings(MEDIA_ROOT="/app/media")  # под твой контейнерный путь
def test_create_property_image(tmp_path):
    # 1) создаём временный файл-изображение внутри MEDIA_ROOT/properties/test.jpg
    media_root = "/app/media"
    rel_path = "properties/test.jpg"
    abs_dir = os.path.join(media_root, "properties")
    abs_path = os.path.join(media_root, rel_path)

    os.makedirs(abs_dir, exist_ok=True)
    img = Image.new("RGB", (2, 2), color=(255, 0, 0))
    img.save(abs_path, format="JPEG")

    # 2) создаём связанные объекты
    ptype = PropertyType.objects.create(name="Billboards", slug="billboard")
    prop = Property.objects.create(
        name="Test Billboard",
        type=ptype,
        description="Big one",
        location="Highway 66",
    )

    # 3) теперь укажем относительный путь, который реально существует
    pic = PropertyImage.objects.create(
        property=prop,
        image=rel_path,
    )

    assert pic.pk is not None
    assert pic.property_id == prop.id
