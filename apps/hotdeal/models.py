#apps/hotdeal/models.py
from django.db import models
from apps.properties.models import Property
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
    section = models.ForeignKey(HotDealSection, on_delete=models.CASCADE, related_name="items")
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name="hot_deal_item")
    title = models.CharField(max_length=255, blank=True)
    additional_description = models.TextField(blank=True)
    promo_1 = models.TextField(blank=True, null=True)
    promo_2 = models.TextField(blank=True, null=True)
    promo_3 = models.TextField(blank=True, null=True)
    promo_4 = models.TextField(blank=True, null=True)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    new_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    badge_text = models.CharField(max_length=50, blank=True)
    badge_percent = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    date_expiry = models.DateField(blank=True, null=True)
    icon = models.ForeignKey('csm.Icon', null=True, blank=True, on_delete=models.SET_NULL)
    button_text = models.CharField(max_length=50, default="Zanechajte žiadosť")
    color_theme = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        ordering = ("order","id")
        constraints = [models.UniqueConstraint(fields=["property"], name="uniq_hotdeal_per_property")]
        
    @builtins.property
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
    
    @builtins.property
    def promo_list(self):
        return [p for p in (self.promo_1, self.promo_2, self.promo_3, self.promo_4) if p]
        
    def __str__(self): return self.title or str(self.property)
