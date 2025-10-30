from django.db import models
from apps.properties.models import Property


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
    description = models.TextField(blank=True)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    new_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    badge_text = models.CharField(max_length=50, blank=True)
    badge_percent = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ("order","id")
        constraints = [models.UniqueConstraint(fields=["property"], name="uniq_hotdeal_per_property")]
    def __str__(self): return self.title or str(self.property)
