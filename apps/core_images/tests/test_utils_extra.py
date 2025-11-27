import io
from pathlib import Path

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from apps.core_images.utils import optimize_image_file
from apps.properties.models import PropertyType, Property, PropertyImage


def make_image_bytes(size=(50, 50), color=(255, 0, 0), fmt="PNG"):
    buf = io.BytesIO()
    img = Image.new("RGB", size, color)
    img.save(buf, format=fmt)
    buf.seek(0)
    return buf.getvalue()


def test_svg_is_skipped():
    svg_content = b"<svg></svg>"
    f = SimpleUploadedFile("icon.svg", svg_content, content_type="image/svg+xml")
    processed, ext = optimize_image_file(f)
    assert processed is None and ext is None


def test_non_image_is_skipped():
    f = SimpleUploadedFile("file.txt", b"not an image", content_type="text/plain")
    processed, ext = optimize_image_file(f)
    assert processed is None and ext is None


@pytest.mark.django_db
def test_mixin_converts_and_downscales(tmp_path, settings):
    # Ensure test media is isolated
    settings.MEDIA_ROOT = tmp_path

    # Given a large JPEG upload
    img_bytes = make_image_bytes(size=(2000, 2000), fmt="JPEG")
    upload = SimpleUploadedFile("big.jpg", img_bytes, content_type="image/jpeg")

    ptype = PropertyType.objects.create(name="Offices", slug="office")
    prop = Property.objects.create(name="Test", type=ptype)
    prop_image = PropertyImage.objects.create(property=prop, image=upload)

    # Reload and inspect the stored file
    prop_image.refresh_from_db()
    stored_path = Path(prop_image.image.name)

    # Saved as webp and downscaled by mixin
    assert stored_path.suffix.lower() == ".webp"

    with Image.open(prop_image.image.path) as out_img:
        assert out_img.width <= 1600
        assert out_img.height <= 1200
