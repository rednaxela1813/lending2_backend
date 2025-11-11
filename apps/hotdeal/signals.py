# apps/hotdeal/signals.py
from datetime import date, timedelta
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from apps.hotdeal.models import HotDealItem
from apps.properties.models import OfficeUnit          # твой класс юнита
from apps.properties.models.mixins import Availability # <— добавили


# ------- helpers -------
def _hotdeal_defaults_from_unit(u) -> dict:
    """Денорм-данные для карточки из юнита любого типа."""
    prop = getattr(u, "property", None)
    desc = (getattr(prop, "summary", "") or getattr(prop, "description", "") or "").strip()
    price = getattr(u, "price_per_month", None) or getattr(u, "price", None)
    area  = getattr(u, "area_sqm", None)

    return {
        "title": str(u),
        "description": desc,
        "new_price": price,
        "additional_description": (f"{int(area)} m²" if area else ""),
        "badge_text": "SALE",
        "badge_percent": 10,
        "is_active": True,
        "date_expiry": date.today() + timedelta(days=30),
        # ⚠️ убрали property_id / property_name — этих полей нет в модели
    }

def _unit_is_free(u) -> bool:
    """Проверка доступности согласно enum'у Availability."""
    val = getattr(u, "availability", None)
    return val == Availability.AVAILABLE     # <— вместо проверки на "Свободно"

def _sync_hotdeal_for_unit(u, *, force_on: bool = False) -> None:
    """
    Создаёт/обновляет HotDealItem для конкретного юнита (GFK).
    force_on=True — показывать всегда (например, для юр-адресов).
    """
    ct = ContentType.objects.get_for_model(u.__class__)

    if not force_on and not _unit_is_free(u):
        HotDealItem.objects.filter(content_type=ct, object_id=u.pk).update(is_active=False)
        return

    defaults = _hotdeal_defaults_from_unit(u)
    obj, created = HotDealItem.objects.get_or_create(
        content_type=ct,
        object_id=u.pk,
        defaults=defaults,
    )
    if not created:
        HotDealItem.objects.filter(pk=obj.pk).update(**defaults)
# ------- /helpers -------


# ------- ресиверы -------
@receiver(post_save, sender=OfficeUnit)
def officeunit_hotdeal(sender, instance: OfficeUnit, **kwargs):
    _sync_hotdeal_for_unit(instance)

@receiver(pre_delete, sender=OfficeUnit)
def officeunit_remove(sender, instance: OfficeUnit, **kwargs):
    ct = ContentType.objects.get_for_model(instance.__class__)
    HotDealItem.objects.filter(content_type=ct, object_id=instance.pk).delete()
# ------- /ресиверы -------
