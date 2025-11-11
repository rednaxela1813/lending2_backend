# apps/hotdeal/context.py
from datetime import date
from typing import List, Dict, Any
from django.urls import reverse
from apps.hotdeal.models import HotDealItem


def build_hot_deal_items() -> List[Dict[str, Any]]:
    """Возвращает список активных карточек HotDealItem для сайта."""
    items: List[Dict[str, Any]] = []

    qs = (
        HotDealItem.objects
        .filter(is_active=True)
        .order_by("id")
    )

    today = date.today()

    for item in qs:
        icon = None
        if getattr(item, "icon_svg", None):
            icon = {
                "svg_inline": item.icon_svg,
                "label": getattr(item, "icon_label", "") or ""
            }

        promo_list = [
            x for x in [
                getattr(item, "promo_1", None),
                getattr(item, "promo_2", None),
                getattr(item, "promo_3", None),
                getattr(item, "promo_4", None),
            ] if x
        ]

        expires_in_days = (item.date_expiry - today).days if getattr(item, "date_expiry", None) else None

        try:
            detail_url = reverse("hotdeal:detail", args=[item.public_id])
        except Exception:
            co = getattr(item, "content_object", None)
            if co and hasattr(co, "resolve_url"):
                try:
                    detail_url = co.resolve_url() or "#contact"
                except Exception:
                    detail_url = "#contact"
            else:
                detail_url = "#contact"

        items.append({
            "public_id": item.public_id,
            "icon": icon,
            "title": item.title,
            "description": (item.description or "").strip(),
            "old_price": getattr(item, "old_price", None),
            "new_price": getattr(item, "new_price", None),
            "additional_description": getattr(item, "additional_description", "") or "",
            "promo_list": promo_list,
            "color_theme": getattr(item, "color_theme", ""),
            "badge_text": getattr(item, "badge_text", "") or "SALE",
            "badge_percent": getattr(item, "badge_percent", None) or 10,
            "expires_in_days": expires_in_days,
            "button_text": getattr(item, "button_text", None) or "Zanechajte žiadosť",
            "resolve_url": detail_url,
        })

    return items
