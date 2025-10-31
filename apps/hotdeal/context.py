# apps/hotdeal/context.py
from datetime import date
from typing import List, Dict, Any
from apps.hotdeal.models import HotDealItem

def build_hot_deal_items() -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    qs = (
        HotDealItem.objects
        .filter(is_active=True, section__is_active=True)
        .select_related("property", "section", "property__type", "icon")  # ⬅️ важно
        .order_by("section__order", "order", "id")
    )

    today = date.today()

    for item in qs:
        p = item.property

        # 1) приоритет — иконка из HotDealItem.icon.svg_inline
        icon = None
        if getattr(item, "icon", None) and getattr(item.icon, "svg_inline", None):
            icon = {
                "svg_inline": item.icon.svg_inline,
                "label": getattr(item.icon, "name", "") or "",
            }
        # 2) фолбэк — иконка из типа Property (если задана)
        elif getattr(p.type, "icon_svg", None):
            icon = {"svg_inline": p.type.icon_svg, "label": p.type.name}

        description = (
            (item.additional_description or "").strip()
            or (getattr(p, "summary", "") or "").strip()
            or (getattr(p, "description", "") or "").strip()
        )

        promo_list = [x for x in [item.promo_1, item.promo_2, item.promo_3, item.promo_4] if x]
        expires_in_days = (item.date_expiry - today).days if item.date_expiry else None

        items.append({
            "icon": icon,                                   # ⬅️ передаём dict с svg_inline
            "title": item.title or p.name,
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
