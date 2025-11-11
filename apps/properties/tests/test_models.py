# apps/properties/tests/test_models.py
import pytest
from apps.properties.models.property import Property, PropertyType, PropertyImage
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


def test_create_property_image(tmp_path, settings):
    media_root = tmp_path / "media"
    settings.MEDIA_ROOT = media_root
    rel_path = "properties/test.jpg"
    abs_path = media_root / rel_path
    abs_path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (2, 2), color=(255, 0, 0))
    img.save(str(abs_path), format="JPEG")

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
