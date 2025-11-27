from django.db import models
from django.urls import reverse
from apps.properties.models import PropertyType
import uuid
from django.urls import NoReverseMatch
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.utils import timezone
from apps.core_images.mixins import ImageOptimizationMixin



class HeroSection(ImageOptimizationMixin, models.Model):
    title = models.CharField(max_length=255) #TODO add uuid for all models
    subtitle = models.TextField(blank=True)
    description = models.TextField(blank=True, null=True, default='Kancelárske priestory, právne adresy a billboardy – všetko na jednom mieste.')
    button_text = models.CharField(max_length=50, default="Оставить заявку")
    right_colon_text = models.CharField(max_length=50, default="Zanechajte žiadosť", blank=True, null=True)   
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='hero_images/', blank=True, null=True)
    IMAGE_FIELDS = ("image",)

    def __str__(self):
        return "Hero Section Content"


class HeaderSection(models.Model):
    logo_text = models.CharField(max_length=100, default='Agentúra Závodský s.r.o.')
    nav_services = models.CharField(max_length=50, default='Služby')
    nav_why = models.CharField(max_length=50, default='Prečo práve my?')
    nav_about = models.CharField(max_length=50, default='O nás')
    nav_contact = models.CharField(max_length=50, default='Kontakt')
    button_text = models.CharField(max_length=50, default='Zanechajte žiadosť')
    updated_at = models.DateTimeField(auto_now=True)
   # images = models.ImageField(upload_to='logo/')

    def __str__(self):
        return "Header Content"
    



class ContactRequest(models.Model):
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.contact})"
    
    
class CarouselImage(ImageOptimizationMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='carousel_images/')
    description = models.CharField(max_length=255, blank=True)
    button_text = models.CharField(max_length=50, default="Explore Offices", blank=True, null=True)
    IMAGE_FIELDS = ("image",)

    def __str__(self):
        return f"Carousel Image {self.id}"
    






class ServiceSection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, default="Naše služby")
    description = models.TextField(blank=True, null=True, default="Kancelárske priestory, právne adresy a billboardy – všetko na jednom mieste."    )
    icon_svg = models.ForeignKey('Icon', blank=True, null=True, on_delete=models.SET_NULL)
    color_icon = models.CharField(max_length=20, default="#2563eb", help_text="Hex color code for the icon")
    property_type = models.ForeignKey(PropertyType, on_delete=models.SET_NULL, null=True, blank=True)  # 🔥 теперь есть
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_list_url(self):
        """
        Link to the general property list filtered by this service type.
        Falls back to None if the route is not configured.
        """
        if not self.property_type:
            return None
        try:
            return f"{reverse('property_list')}?type={self.property_type.slug}"
        except NoReverseMatch:
            return None


    def __str__(self):
        return self.title



class FrontendTheme(models.Model):
    name = models.CharField(max_length=100, default="Default")

    # Фон
    navbar_background = models.CharField(max_length=20, default="#ffffff")
    body_background = models.CharField(max_length=20, default="#f9fafb")
    footer_background = models.CharField(max_length=20, default="#f1f5f9")

    # Текст
    text_color = models.CharField(max_length=20, default="#111827")
    text_hover_color = models.CharField(max_length=20, default="#1e40af")

    # Границы
    border_color = models.CharField(max_length=20, default="#d1d5db")
    border_hover_color = models.CharField(max_length=20, default="#9ca3af")

    # Основной цвет (например, для кнопок)
    primary_color = models.CharField(max_length=20, default="#2563eb")
    primary_hover_color = models.CharField(max_length=20, default="#1d4ed8")

    # Активация
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    



class Icon(ImageOptimizationMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.SlugField(max_length=100, unique=True)        # 'office', 'billboard', 'legal', ...
    label = models.CharField(max_length=100, blank=True)
    svg_inline = models.TextField(blank=True)                  # <svg>...</svg> — удобнее и быстрее
    image = models.ImageField(upload_to="icons/", blank=True, null=True)
    css_class = models.CharField(max_length=120, blank=True)   # если хочешь использовать icon-font
    IMAGE_FIELDS = ("image",)

    def __str__(self):
        return self.label or self.key
    
    
    

    
class BottomCTASection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, default="Máte otázky?")
    subtitle = models.TextField(blank=True, null=True, default="Kontaktujte nás ešte dnes a získajte viac informácií o našich službách a ponukách.")
    button_text = models.CharField(max_length=50, default="Zanechajte žiadosť")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Bottom CTA Section Content"
