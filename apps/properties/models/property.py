#apps/properties/models/property.py
import re
import uuid
from urllib.parse import urlparse, quote_plus

from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import slugify

from apps.core_images.mixins import ImageOptimizationMixin
from apps.properties.models.mixins import AvailabilityMixin



class PropertyType(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    #icon_svg = models.TextField(blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def _generate_unique_slug(self) -> str:
        base = slugify(self.name) or "type"
        candidate = base
        suffix = 1
        while PropertyType.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
            suffix += 1
            candidate = f"{base}-{suffix}"
        return candidate

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)
    


class Property(AvailabilityMixin,models.Model):
    
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    type = models.ForeignKey(PropertyType, on_delete=models.PROTECT, related_name='properties')    
    description = models.TextField(blank=True)
    list_details = models.JSONField(max_length=1044, blank=True, default=list, help_text="Detaily pre zobrazenie v zozname")
    summary = models.CharField(max_length=255, blank=True, help_text="Krátky popis")
    location = models.CharField(max_length=255, blank=True)
    map_embed_url = models.URLField(
        max_length=1024,
        blank=True,
        help_text="Plný URL na Google Maps embed (bez HTML)",
    )
    iframe = models.TextField(blank=True, help_text="HTML iframe  Google Maps (legacy, už sa nepoužíva priamo)")
    created_at = models.DateTimeField(auto_now_add=True)

    

    #busy_until = models.DateField(blank=True, null=True, help_text="Ak je nehnuteľnosť obsadená, do kedy?")
    #price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Cena za prenájom (ak je relevantné)")
   # currency = models.CharField(max_length=10, default='EUR', help_text="Mena ceny", blank=True, null=True)
    
    
    def clean(self):
        super().clean()

        if self.iframe:
            self.iframe = self.iframe.replace('width="600"', '').replace('height="450"', '')

        if self.map_embed_url:
            parsed = urlparse(self.map_embed_url)
            if parsed.scheme not in ("http", "https") or parsed.netloc not in {"www.google.com", "google.com", "maps.google.com"}:
                from django.core.exceptions import ValidationError
                raise ValidationError({"map_embed_url": "Len Google Maps embed URL je povolené."})

    @staticmethod
    def _extract_iframe_src(raw_iframe: str) -> str | None:
        """Return src value from stored iframe HTML if present."""
        if not raw_iframe:
            return None
        match = re.search(r'src=["\\\']([^"\\\']+)["\\\']', raw_iframe)
        return match.group(1) if match else None

    @staticmethod
    def _is_allowed_map_src(url: str) -> bool:
        parsed = urlparse(url)
        return parsed.scheme in {"http", "https"} and parsed.netloc in {"www.google.com", "google.com", "maps.google.com"}

    @property
    def embed_src(self) -> str:
        """
        Safe embed URL to use in templates. Prefers explicit embed URL,
        falls back to extracted src from legacy iframe, then location search.
        """
        if self.map_embed_url:
            return self.map_embed_url

        legacy_src = self._extract_iframe_src(self.iframe or "")
        if legacy_src and self._is_allowed_map_src(legacy_src):
            return legacy_src

        if self.location:
            query = quote_plus(self.location)
            return f"https://www.google.com/maps?q={query}&output=embed"

        return ""
    
    
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
    
