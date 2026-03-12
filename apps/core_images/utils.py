#apps/core_images/utils.py
import io
import os
from typing import Optional, Tuple

from django.core.files.base import ContentFile
from PIL import Image, ImageOps

SKIP_EXTS = {".svg"}  # вектор не трогаем

def optimize_image_file(
    django_file,
    *,
    max_w: int = 1600,
    max_h: int = 1200,
    target_format: str = "WEBP",  # "WEBP" | "JPEG"
    quality: int = 80,
    only_downscale: bool = True,
    keep_exif: bool = False,
    ) -> Tuple[Optional[ContentFile], Optional[str]]:
    """
    Принимает FieldFile.file (или UploadedFile). Возвращает (ContentFile, new_ext)
    или (None, None), если менять не нужно/нельзя.
    """
    name = getattr(django_file, "name", "") or ""
    ext = os.path.splitext(name)[1].lower()
    if ext in SKIP_EXTS:
        return None, None

    # читаем в память (работает и с S3/MinIO)
    try:
        django_file.seek(0)
    except Exception:
        pass

    data = django_file.read()
    if not data:
        return None, None

    try:
        img = Image.open(io.BytesIO(data))
    except Exception:
        return None, None  # не картинка

    # нормализуем режим
    if img.mode in ("P", "PA", "LA"):
        img = img.convert("RGBA")
    elif img.mode == "L":
        img = img.convert("RGB")

    # даунскейл (без апскейла)
    if not only_downscale or (img.width > max_w or img.height > max_h):
        img = ImageOps.contain(img, (max_w, max_h), method=Image.Resampling.LANCZOS)

    # выбор формата
    def pick():
        if target_format.upper() == "JPEG":
            if "A" in img.getbands() or img.mode in ("RGBA", "LA"):
                return "WEBP", ".webp"
            return "JPEG", ".jpg"
        return "WEBP", ".webp"

    out_fmt, new_ext = pick()

    buf = io.BytesIO()
    save_kwargs = {}
    exif = img.info.get("exif") if keep_exif else None
    icc = img.info.get("icc_profile") if keep_exif else None

    if out_fmt == "WEBP":
        save_kwargs.update(dict(format="WEBP", quality=quality, method=6))
    else:
        if img.mode != "RGB":
            bg = Image.new("RGB", img.size, (255, 255, 255))
            if "A" in img.getbands():
                bg.paste(img, mask=img.split()[3])
            else:
                bg.paste(img)
            img = bg
        save_kwargs.update(dict(format="JPEG", quality=quality, optimize=True, progressive=True))

    if exif: save_kwargs["exif"] = exif
    if icc:  save_kwargs["icc_profile"] = icc

    try:
        img.save(buf, **save_kwargs)
    except OSError:
        # если Pillow ругается на exif/icc
        save_kwargs.pop("exif", None)
        save_kwargs.pop("icc_profile", None)
        buf = io.BytesIO()
        img.save(buf, **save_kwargs)

    out = buf.getvalue()
    if len(out) >= len(data):
        return None, None  # не ухудшаем

    return ContentFile(out), new_ext
