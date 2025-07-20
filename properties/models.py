# properties/models.py
import uuid
from django.db import models
from django.utils.html import format_html
import os
from PIL import Image
from django.urls import reverse


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
    list_details = models.JSONField(blank=True, default=list, help_text="Detaily pre zobrazenie v zozname")
    summary = models.CharField(max_length=255, blank=True, help_text="Krátky popis")
    location = models.CharField(max_length=255, blank=True)
    iframe = models.TextField(blank=True, help_text="HTML iframe  Google Maps")
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def get_absolute_url(self):
        if self.type == 'office':
            return reverse('office_detail', kwargs={'public_id': self.public_id})
        elif self.type == 'address':
            return reverse('address_detail', kwargs={'public_id': self.public_id})
        elif self.type == 'billboard':
            return reverse('billboard_detail', kwargs={'public_id': self.public_id})
        

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
