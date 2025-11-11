# apps/core_images/tests/test_optimize.py
import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.core_images.utils import optimize_image_file


def test_optimize_reduces_size_for_large_jpeg():
    # создаём большую картинку в памяти
    img = Image.new("RGB", (3000, 2000), (200, 200, 200))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=95)
    data = buf.getvalue()

    up = SimpleUploadedFile("test.jpg", data, content_type="image/jpeg")
    cf, ext = optimize_image_file(up.file, max_w=1600, max_h=1200, target_format="WEBP", quality=80)
    assert cf is not None
    assert ext == ".webp"
    assert len(cf.read()) < len(data)
