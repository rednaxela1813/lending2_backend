# properties/models.py
import uuid
from django.db import models
from django.utils.html import format_html
import os
from PIL import Image
from django.urls import reverse



class PropertyType(models.Model):
    type_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    icon_svg = models.TextField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    


class Property(models.Model):
    

    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    type = models.ForeignKey(PropertyType, on_delete=models.PROTECT, related_name='properties')    
    description = models.TextField(blank=True)
    list_details = models.JSONField(blank=True, default=list, help_text="Detaily pre zobrazenie v zozname")
    summary = models.CharField(max_length=255, blank=True, help_text="Krátky popis")
    location = models.CharField(max_length=255, blank=True)
    iframe = models.TextField(blank=True, help_text="HTML iframe  Google Maps")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        # Удаляем width и height из iframe
        if self.iframe:
            self.iframe = self.iframe.replace('width="600"', '').replace('height="450"', '')
    
    
    def get_absolute_url(self):
        return reverse('property_detail', kwargs={'public_id': self.public_id})


        

    def __str__(self):
        return f"{self.type}: {self.name}"  

    
    

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Изображение для {self.property.name}"
    
    def preview(self):
        if self.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; border-radius: 8px; box-shadow: 0 0 5px #ccc;" />',
                self.image.url
            )
        return "(нет изображения)"
    preview.short_description = "Превью"
    #preview.allow_tags = True  # Django < 2.0 не нужен в >=2.0

    def save(self, *args, **kwargs):
        # Сначала сохраняем оригинал (чтобы файл появился на диске)
        super().save(*args, **kwargs)

        # Путь к файлу изображения
        img_path = self.image.path
        img = Image.open(img_path)

        # 💡 Уменьшаем изображение, если оно слишком большое
        max_size = (1600, 1200)
        img.thumbnail(max_size, Image.LANCZOS)

        # 💡 Конвертируем в WebP
        webp_path = os.path.splitext(img_path)[0] + '.webp'
        img.save(webp_path, 'WEBP', quality=80)  # quality=80 – баланс вес/качество

        # ❗ Удаляем оригинальный файл
        if img_path != webp_path and os.path.exists(img_path):
            os.remove(img_path)

        # Меняем имя файла в поле image (чтобы оно указывало на .webp)
        self.image.name = os.path.splitext(self.image.name)[0] + '.webp'

        # Сохраняем снова, чтобы обновить путь к файлу в БД
        super().save(update_fields=['image'])


# properties/models.py

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

class OfficeUnitImage(models.Model):
    office_unit = models.ForeignKey(
        'OfficeUnit',
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='office_unit_images/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Obrázok kancelárie {self.office_unit}"

    def preview(self):
        if self.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; border-radius: 8px; box-shadow: 0 0 5px #ccc;" />',
                self.image.url
            )
        return "(bez obrázka)"

    preview.short_description = "Náhľad"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img_path = self.image.path
        img = Image.open(img_path)

        # Уменьшаем изображение
        max_size = (1600, 1200)
        img.thumbnail(max_size, Image.LANCZOS)

        # Сохраняем как webp
        webp_path = os.path.splitext(img_path)[0] + '.webp'
        img.save(webp_path, 'WEBP', quality=80)

        if img_path != webp_path and os.path.exists(img_path):
            os.remove(img_path)

        self.image.name = os.path.splitext(self.image.name)[0] + '.webp'
        super().save(update_fields=['image'])



