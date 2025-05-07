# properties/models.py
import uuid
from django.db import models
from django.utils.html import format_html

class Property(models.Model):
    PROPERTY_TYPES = [
        ('office', 'Kancelária'),
        ('address', 'Sydlo'),
        ('billboard', 'Billboard'),
    ]

    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    description = models.TextField(blank=True)
    summary = models.CharField(max_length=255, blank=True, help_text="Krátky popis")
    location = models.CharField(max_length=255, blank=True)
    iframe = models.TextField(blank=True, help_text="HTML iframe  Google Maps")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_display()}: {self.name}"
    
    

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Изображение для {self.property.name}"
    
    def preview(self):
        if self.image:
            return format_html('<img src="{}" style="max-height: 100px;" />', self.image.url)
        return ""
    preview.short_description = "Превью"
