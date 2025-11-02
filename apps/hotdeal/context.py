from datetime import date
from django.db import models
from django.db.models import Q
from typing import List, Dict, Any, Optional
from apps.hotdeal.models import HotDealItem
from accounting.models import Company


def build_hot_deal_items(*, company: Optional["Company"] = None) -> List[Dict[str, Any]]:
    """
    company = None → показываем только глобальные (company IS NULL)
    company = X   → показываем (company=X) И глобальные (company IS NULL)
    """
    items: List[Dict[str, Any]] = []
    qs = (
    HotDealItem.objects
    .filter(is_active=True, section__is_active=True)
    .select_related("property", "section", "property__type")
    .order_by("section__order", "id")  # убрали "order"
)

    if company is None:
        qs = qs.filter(company__isnull=True)
    else:
        qs = qs.filter(Q(company=company) | Q(company__isnull=True))  # ← вот тут просто Q

    today = date.today()

    for item in qs:
        p = item.property

        # приоритет: item.icon.svg_inline → fallback: p.type.icon_svg
        svg_inline = None
        if getattr(item, "icon", None) and getattr(item.icon, "svg_inline", None):
            svg_inline = item.icon.svg_inline
        elif getattr(getattr(p, "type", None), "icon_svg", None):
            svg_inline = p.type.icon_svg

        icon = {"svg_inline": svg_inline, "label": getattr(p.type, "name", "")} if svg_inline else None

        description = (
            (getattr(p, "summary", "") or "").strip()
              or (getattr(p, "description", "") or "").strip()
        )
        promo_list = [x for x in [item.promo_1, item.promo_2, item.promo_3, item.promo_4] if x]
        expires_in_days = (item.date_expiry - today).days if item.date_expiry else None

        items.append({
            "icon": icon,
            "title": item.title or getattr(p, "name", ""),
            "description": description,
            "old_price": item.old_price,
            "new_price": item.new_price,
            "additional_description": item.additional_description or "",
            "promo_list": promo_list,
            "color_theme": item.color_theme,
            "badge_text": item.badge_text or "SALE",
            "badge_percent": item.badge_percent or 10,
            "expires_in_days": expires_in_days,
            "button_text": item.button_text or "Zanechajte žiadosť",
            "resolve_url": getattr(item, "resolve_url", lambda: "#contact")(),
        })

    return items
