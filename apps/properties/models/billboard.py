import uuid
from django.db import models
from django.utils.html import format_html
from apps.core_images.mixins import ImageOptimizationMixin
from .property import Property
from .mixins import AvailabilityMixin



class BillboardUnit(AvailabilityMixin, models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='billboards')
    location_description = models.CharField(max_length=255, blank=True)
    size = models.CharField(max_length=100, blank=True, help_text="Rozmer (napr. 5x2 m)")
    visibility = models.CharField(max_length=255, blank=True, help_text="Viditeľnosť alebo orientácia")
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['property__name', 'id']

    def __str__(self):
        return f"Billboard {self.size or ''} – {self.property.name}"


class BillboardUnitImage(ImageOptimizationMixin, models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    billboard_unit = models.ForeignKey(BillboardUnit, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='billboard_images/')
    description = models.CharField(max_length=255, blank=True)

    IMAGE_FIELDS = ("image",)
    IMAGE_OPT_KWARGS = dict(max_w=1600, max_h=1200, target_format="WEBP", quality=80, only_downscale=True)

    def preview(self):
        if self.image:
            return format_html('<img src="{}" style="max-height:100px;border-radius:8px;box-shadow:0 0 4px #ccc;">', self.image.url)
        return "(нет изображения)"
    preview.short_description = "Preview"
