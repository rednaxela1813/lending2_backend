from django.db import models
from django.urls import reverse
from properties.models import PropertyType
import uuid
from django.urls import NoReverseMatch
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.utils import timezone


class HeroSection(models.Model):
    title = models.CharField(max_length=255) #TODO add uuid for all models
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
    



    
    
    
    
    
class HotDealItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)   
    
    
    # Текст/цены для карточки (можно переопределить независимо от Property)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    new_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    additional_description = models.TextField(blank=True, null=True)
    promo_1 = models.TextField(blank=True, null=True)
    promo_2 = models.TextField(blank=True, null=True)
    promo_3 = models.TextField(blank=True, null=True)
    promo_4 = models.TextField(blank=True, null=True)

    badge_text = models.CharField(max_length=50, default="Zľava", help_text="текст в круглом бейдже")
    badge_percent = models.PositiveIntegerField(default=20)
    date_expiry = models.DateField(blank=True, null=True)
    button_text = models.CharField(max_length=50, default="Zanechajte žiadosť")
    
    color_theme = models.CharField(max_length=50, blank=True, null=True)
    
    # управление порядком вывода
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "-updated_at"]

    def __str__(self):
        return f"HotDealItem - {self.title}"

    @property
    def expires_in_days(self):
        if not self.date_expiry:
            return None
        return (self.date_expiry - timezone.now().date()).days

    def resolve_url(self):
        """
        Возвращаем URL карточки:
        - если у Property есть get_absolute_url — используем его,
        - иначе — '#contact' как запасной вариант.
        """
        try:
            if self.property and hasattr(self.property, "get_absolute_url"):
                return self.property.get_absolute_url()
        except Exception:
            pass
        return "#contact"