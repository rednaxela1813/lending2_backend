# apps/hotdeal/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from apps.properties.models import Property
from apps.properties.models.mixins import Availability
from .models import HotDealItem, HotDealSection


def _default_section() -> HotDealSection:
    """
    Возвращает первую секцию (по id) либо создаёт дефолтную.
    В модели HotDealSection больше НЕТ полей is_active/order/name,
    поэтому используем существующие: title/description/additional_description.
    """
    s = HotDealSection.objects.order_by("id").first()
    if s:
        return s
    return HotDealSection.objects.create(
        title="Hot Deals",
        description="Aktuálne špeciálne ponuky",
        additional_description="",
    )


@receiver(post_save, sender=Property)
def sync_hotdeal_on_property_change(sender, instance: Property, **kwargs):
    """
    Если объект доступен (AVAILABLE) — гарантируем наличие активного HotDealItem,
    иначе выключаем все HotDealItem по этому объекту.
    """
    if instance.availability == Availability.AVAILABLE:
        item, created = HotDealItem.objects.get_or_create(
            property=instance,
            defaults={
                "section": _default_section(),
                "title": str(instance),
                "is_active": True,
            },
        )
        # если уже был, но выключен — включаем
        if not created and not item.is_active:
            item.is_active = True
            item.save(update_fields=["is_active"])
    else:
        # деликатнее: выключаем активные, если объект недоступен
        HotDealItem.objects.filter(property=instance, is_active=True).update(is_active=False)


