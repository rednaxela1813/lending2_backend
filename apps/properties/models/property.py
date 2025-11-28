#apps/properties/models/property.py
import uuid
from django.db import models
from django.utils.html import format_html
from apps.properties.models.mixins import AvailabilityMixin



from django.urls import reverse
from apps.core_images.mixins import ImageOptimizationMixin



class PropertyType(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    #icon_svg = models.TextField(blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    


class Property(AvailabilityMixin,models.Model):
    
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    type = models.ForeignKey(PropertyType, on_delete=models.PROTECT, related_name='properties')    
    description = models.TextField(blank=True)
    list_details = models.JSONField(max_length=1044, blank=True, default=list, help_text="Detaily pre zobrazenie v zozname")
    summary = models.CharField(max_length=255, blank=True, help_text="Krátky popis")
    location = models.CharField(max_length=255, blank=True)
    iframe = models.TextField(blank=True, help_text="HTML iframe  Google Maps")
    created_at = models.DateTimeField(auto_now_add=True)

    

    busy_until = models.DateField(blank=True, null=True, help_text="Ak je nehnuteľnosť obsadená, do kedy?")
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Cena za prenájom (ak je relevantné)")
    currency = models.CharField(max_length=10, default='EUR', help_text="Mena ceny", blank=True, null=True)
    
    
    def clean(self):
        # Удаляем width и height из iframe
        if self.iframe:
            self.iframe = self.iframe.replace('width="600"', '').replace('height="450"', '')
    
    
    def get_absolute_url(self):
        return reverse('property_detail', kwargs={'public_id': self.public_id})


        

    def __str__(self):
        return f"{self.type}: {self.name}"  

    
    

class PropertyImage(ImageOptimizationMixin, models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    description = models.CharField(max_length=255, blank=True)
    
    IMAGE_FIELDS = ("image",)
    IMAGE_OPT_KWARGS = dict(max_w=1600, max_h=1200, target_format="WEBP", quality=80, only_downscale=True)


    def __str__(self):
        return f"Изображение для {self.property.name}"
    
    def preview(self):
        if self.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; border-radius: 8px; box-shadow: 0 0 5px #ccc;" />',
                self.image.url
            )
        return "(нет изображения)"
    preview.short_description = "Preview"
    
