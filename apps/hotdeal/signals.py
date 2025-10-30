#apps/hotdeal/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.properties.models import Property
from apps.properties.models.mixins import Availability
from .models import HotDealItem, HotDealSection



def _default_section():
    s = HotDealSection.objects.filter(is_active=True).order_by("order","id").first()
    if not s:
        s = HotDealSection.objects.create(name="Default", is_active=True, order=0)
    return s


@receiver(post_save, sender=Property)
def sync_hotdeal_on_property_change(sender, instance: Property, **kwargs):
    if instance.availability == Availability.AVAILABLE:
        item, _ = HotDealItem.objects.get_or_create(
            property=instance,
            defaults={"section": _default_section(), "title": str(instance)}
        )
        if not item.is_active:
            item.is_active = True
            item.save(update_fields=["is_active"])
    else:
        HotDealItem.objects.filter(property=instance, is_active=True).update(is_active=False)
