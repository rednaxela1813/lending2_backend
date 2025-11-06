#apps/hotdeal/models.py
from django.db import models
from django.db.models import Q 
from django.utils import timezone
import builtins
import uuid
from django.urls import reverse

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType






class HotDealSection(models.Model):
    title = models.CharField(max_length=255)
    additional_description = models.TextField(blank=True, default="")
    description = models.TextField(blank=True, default="")
    
    class Meta:
        ordering = ("id",)
    def __str__(self): return self.title



class HotDealItem(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
   # section = models.ForeignKey("HotDealSection", on_delete=models.CASCADE)
   # property = models.ForeignKey("properties.Property", on_delete=models.CASCADE)
   # company = models.ForeignKey("accounting.Company", null=True, blank=True, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    # контент карточки
    title = models.CharField(max_length=255)
    additional_description = models.TextField(blank=True, default="")
    description = models.TextField(blank=True, default="")
    
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    new_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # промо-пункты (например: «Wi-Fi», «Parking»)
    promo_1 = models.CharField(max_length=255, blank=True)
    promo_2 = models.CharField(max_length=255, blank=True)
    promo_3 = models.CharField(max_length=255, blank=True)
    promo_4 = models.CharField(max_length=255, blank=True)

    # базовые свойства
    is_active = models.BooleanField(default=True)
    date_expiry = models.DateField(blank=True, null=True)

    # визуальные настройки
    color_theme = models.CharField(max_length=50, blank=True)
    badge_text = models.CharField(max_length=50, blank=True)
    badge_percent = models.PositiveIntegerField(blank=True, null=True)
    button_text = models.CharField(max_length=100, blank=True)
    icon = models.ForeignKey(
        "csm.Icon",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="hotdeal_items",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["content_type", "object_id"],
                name="uniq_hotdeal_per_unit",
            ),
        ]
    ordering = [ "id"]

    def __str__(self):
        return self.title

    @builtins.property
    def expires_in_days(self):
        if not self.date_expiry:
            return None
        return (self.date_expiry - timezone.now().date()).days
    

    def resolve_url(self):                     
        try:
            return self.get_absolute_url()      
        except Exception:
            pass
        try:
            if self.property and hasattr(self.property, "get_absolute_url"):
                return self.property.get_absolute_url()
        except Exception:
            pass
        return "#contact"

    @builtins.property
    def promo_list(self):
        """Собирает непустые promo_X в список."""
        return [p for p in (self.promo_1, self.promo_2, self.promo_3, self.promo_4) if p]
    
    def get_absolute_url(self):
        return reverse("hotdeal:detail", args=[self.public_id])
    