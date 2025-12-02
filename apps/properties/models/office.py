#apps/properties/models/office.py
import builtins
import uuid
from django.db import models
from django.utils.html import format_html
from django.urls import reverse
from apps.core_images.mixins import ImageOptimizationMixin
from .property import Property
from apps.properties.models.mixins import AvailabilityMixin



class OfficeUnit(AvailabilityMixin, models.Model):

    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='office_units')

    floor = models.IntegerField(help_text="Číslo poschodia (napr. 0 = prízemie, 1 = prvé poschodie)")
    unit_number = models.CharField(max_length=50, help_text="Číslo kancelárie alebo identifikátor")
    area_sqm = models.FloatField(help_text="Rozloha v m²")
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2, help_text="Cena za mesiac (€)")

    description = models.TextField(blank=True)
    
    map_embed_url = models.URLField(
        max_length=1024,
        blank=True,
        help_text="Plný URL na Google Maps embed (bez HTML)",
    )
    iframe = models.TextField(blank=True, help_text="HTML iframe z Google Maps pre túto jednotku (legacy)")

    class Meta:
        unique_together = ('property', 'floor', 'unit_number')
        ordering = ['floor', 'unit_number']

    def __str__(self):
        return f"{self.property.name} – Poschodie {self.floor}, Kancelária {self.unit_number}"

    @builtins.property
    def embed_src(self) -> str:
        """
        Safe embed URL for templates. Prefers own embed URL,
        then legacy iframe src if allowed, then property's embed.
        """
        if self.map_embed_url:
            return self.map_embed_url

        legacy_src = Property._extract_iframe_src(self.iframe or "")
        if legacy_src and Property._is_allowed_map_src(legacy_src):
            return legacy_src

        if self.property:
            return self.property.embed_src

        return ""



# properties/models.py

class OfficeUnitImage(ImageOptimizationMixin, models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    office_unit = models.ForeignKey(
        'OfficeUnit',
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='office_unit_images/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Obrázok kancelárie {self.office_unit}"

    IMAGE_FIELDS = ("image",)
    IMAGE_OPT_KWARGS = dict(max_w=1600, max_h=1200, target_format="WEBP", quality=80, only_downscale=True)
    
    def preview(self):
        if self.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; border-radius: 8px; box-shadow: 0 0 5px #ccc;" />',
                self.image.url
            )
        return "(нет изображения)"
    preview.short_description = "Preview"
