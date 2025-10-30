import uuid
from django.db import models
from django.utils.html import format_html
import os
from PIL import Image
from django.urls import reverse
from apps.core_images.mixins import ImageOptimizationMixin
from .property import Property




class OfficeUnit(models.Model):
    STATUS_CHOICES = [
        ('available', 'Voľné'),
        ('occupied', 'Obsadené'),
    ]

    property = models.ForeignKey(
    Property,
    on_delete=models.CASCADE,
    related_name='office_units',
)
    floor = models.IntegerField(help_text="Číslo poschodia (napr. 0 = prízemie, 1 = prvé poschodie)")
    unit_number = models.CharField(max_length=50, help_text="Číslo kancelárie alebo identifikátor")
    area_sqm = models.FloatField(help_text="Rozloha v m²")
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2, help_text="Cena za mesiac (€)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('property', 'floor', 'unit_number')
        ordering = ['floor', 'unit_number']

    def __str__(self):
        return f"{self.property.name} – Poschodie {self.floor}, Kancelária {self.unit_number}"



# properties/models.py

class OfficeUnitImage(ImageOptimizationMixin, models.Model):
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



