# apps/hotdeal/context.py
from datetime import date
from typing import List, Dict, Any, Optional

from django.db.models import Q
from django.urls import reverse

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
        .filter(is_active=True)
        .select_related("property", "section", "property__type")
        .order_by("id")
    )

    if company is None:
        qs = qs.filter(company__isnull=True)
    else:
        qs = qs.filter(Q(company=company) | Q(company__isnull=True))

    today = date.today()

    for item in qs:
        p = getattr(item, "property", None)
        p_type = getattr(p, "type", None)

        # приоритет: item.icon.svg_inline → fallback: p.type.icon_svg
        svg_inline = None
        icon_label = ""
        if getattr(item, "icon", None) and getattr(item.icon, "svg_inline", None):
            svg_inline = item.icon.svg_inline
            icon_label = getattr(p_type, "name", "") or ""
        elif getattr(p_type, "icon_svg", None):
            svg_inline = p_type.icon_svg
            icon_label = getattr(p_type, "name", "") or ""

        icon = {"svg_inline": svg_inline, "label": icon_label} if svg_inline else None

        # краткое описание: summary → description
        description = (
            (getattr(p, "summary", "") or "").strip()
            or (getattr(p, "description", "") or "").strip()
        )

        promo_list = [x for x in [item.promo_1, item.promo_2, item.promo_3, item.promo_4] if x]
        expires_in_days = (item.date_expiry - today).days if item.date_expiry else None

        # ссылка на полную страницу hot-deal (если маршрут подключён)
        try:
            detail_url = reverse("hotdeal:detail", args=[item.public_id])
        except Exception:
            # если detail-роута нет, попробуем URL связанного объекта
            if hasattr(item, "resolve_url"):
                detail_url = item.resolve_url() or "#contact"
            else:
                detail_url = "#contact"

        items.append({
            # ⬇️ КЛЮЧЕВОЕ: нужен для {% url 'hotdeal:partial' item.public_id %}
            "public_id": item.public_id,

            "icon": icon,
            "title": item.title or (getattr(p, "name", "") or ""),
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
            # можно использовать в местах, где нужна обычная ссылка
            "resolve_url": detail_url,
        })

    return items
