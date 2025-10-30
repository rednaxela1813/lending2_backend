import os
from django.db import models
from apps.core_images.utils import optimize_image_file


class ImageOptimizationMixin(models.Model):
    """
    Подключи к модели и задай:
      IMAGE_FIELDS = ("image", "logo", ...)
      IMAGE_OPT_KWARGS = {...}  # опционально
    """
    IMAGE_FIELDS: tuple[str, ...] = ()
    IMAGE_OPT_KWARGS: dict = {}

    class Meta:
        abstract = True

    def _optimize_field(self, field_name: str) -> bool:
        f = getattr(self, field_name, None)
        if not f or not getattr(f, "name", None) or not hasattr(f, "file"):
            return False
        try:
            f.file.seek(0)
        except Exception:
            pass

        cf, new_ext = optimize_image_file(f.file, **self.IMAGE_OPT_KWARGS)
        if cf is None:
            return False

        base, _ = os.path.splitext(f.name)
        f.save(f"{base}{new_ext}", cf, save=False)
        return True

    def save(self, *args, **kwargs):
        for fn in self.IMAGE_FIELDS:
            try:
                self._optimize_field(fn)
            except Exception:
                # не валим сохранение из-за одной картинки
                pass
        return super().save(*args, **kwargs)
