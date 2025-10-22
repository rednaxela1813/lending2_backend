from django.db import models
from django.urls import reverse
from properties.models import PropertyType
import uuid
from django.urls import NoReverseMatch


class HeroSection(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.TextField(blank=True)
    description = models.TextField(blank=True, null=True, default='Kancelárske priestory, právne adresy a billboardy – všetko na jednom mieste.')
    button_text = models.CharField(max_length=50, default="Оставить заявку")
    right_colon_text = models.CharField(max_length=50, default="Zanechajte žiadosť", blank=True, null=True)   
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='hero_images/', blank=True, null=True)

    def __str__(self):
        return "Hero Section Content"


class HeaderSection(models.Model):
    logo_text = models.CharField(max_length=100, default='Agentúra Závodský s.r.o.')
    nav_services = models.CharField(max_length=50, default='Služby')
    nav_why = models.CharField(max_length=50, default='Prečo práve my?')
    nav_contact = models.CharField(max_length=50, default='Kontakt')
    button_text = models.CharField(max_length=50, default='Zanechajte žiadosť')
    updated_at = models.DateTimeField(auto_now=True)
    images = models.ImageField(upload_to='logo/')

    def __str__(self):
        return "Header Content"


class FooterInfo(models.Model):
    about_title = models.CharField(max_length=100, default="Agentúra Závodský")
    about_description = models.TextField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=30)
    contact_address = models.CharField(max_length=255)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Footer Info"
    

class CompanyInfo(models.Model):
    name = models.CharField(max_length=255)
    ico = models.CharField("IČO", max_length=20, blank=True)
    dic = models.CharField("DIČ", max_length=20, blank=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Informácie o firme"
        verbose_name_plural = "Informácie o firme"

    def __str__(self):
        return self.name
    
    



class ContactRequest(models.Model):
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.contact})"
    
    
class CarouselImage(models.Model):
    image = models.ImageField(upload_to='carousel_images/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Carousel Image {self.id}"
    






class ServiceSection(models.Model):
    

    title = models.CharField(max_length=255, default="Naše služby")
    description = models.TextField(blank=True, null=True, default="Kancelárske priestory, právne adresy a billboardy – všetko na jednom mieste."    )
    icon_svg = models.TextField(blank=True)  # если нужно
    property_type = models.ForeignKey(PropertyType, on_delete=models.SET_NULL, null=True, blank=True)  # 🔥 теперь есть
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def get_list_url(self):
        if self.property_type:
            slug = self.property_type.slug
            try:
                # если есть роут с параметром
                return reverse('property_list', kwargs={'type': slug})
            except NoReverseMatch:
                # fallback: базовый путь + ?type=slug
                base = reverse('property_list')
                return f"{base}?type={slug}"
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
