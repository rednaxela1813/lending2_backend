#apps/hotdeal/models.py
from django.db import models
from django.db.models import Q 

from django.utils import timezone
import builtins





class HotDealSection(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ("order","id")
    def __str__(self): return self.name
    
    

class HotDealItem(models.Model):
    section = models.ForeignKey("HotDealSection", on_delete=models.CASCADE)
    property = models.ForeignKey("properties.Property", on_delete=models.CASCADE)
    company = models.ForeignKey("accounting.Company", null=True, blank=True, on_delete=models.CASCADE)

    # контент карточки
    title = models.CharField(max_length=255)
    additional_description = models.TextField(blank=True, default="")
    
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
            fields=["section", "property", "company"],
            name="uniq_hotdeal_per_section_property_company",
        ),
        # Удаляем старый constraint с condition — он конфликтует
    ]
    ordering = ["section__order", "id"]

    def __str__(self):
        return self.title

    @builtins.property
    def expires_in_days(self):
        if not self.date_expiry:
            return None
        return (self.date_expiry - timezone.now().date()).days

    def resolve_url(self):
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