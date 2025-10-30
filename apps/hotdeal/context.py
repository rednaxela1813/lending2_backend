# apps/hotdeal/context.py
from datetime import date
from typing import List, Dict, Any

from apps.hotdeal.models import HotDealItem


def build_hot_deal_items() -> List[Dict[str, Any]]:
    """
    Готовит список словарей под шаблон HotDealsSection.html.
    Берём только активные элементы в активных секциях,
    тянем связанные property/section одним запросом.
    """
    items: List[Dict[str, Any]] = []
    qs = (
        HotDealItem.objects
        .filter(is_active=True, section__is_active=True)
        .select_related("property", "section")
        .order_by("section__order", "order", "id")
    )

    today = date.today()

    for item in qs:
        p = item.property  # apps.properties.models.Property
        # Тут можно из Property/Type вытянуть иконку/цвет/промо и т.п.
        # Ставим разумные фолбэки, чтобы шаблон не падал.
        icon = None
        if getattr(p.type, "icon_svg", None):
            icon = {"svg_inline": p.type.icon_svg, "label": p.type.name}
        # color_theme — если у тебя хранится в БД; иначе None
        color_theme = getattr(p, "color_theme", None)

        # Пример «акции до даты»: если захочешь — добавь поле date_expiry в HotDealItem
        expires_in_days = None
        if hasattr(item, "date_expiry") and item.date_expiry:
            expires_in_days = (item.date_expiry - today).days

        # Промо-пункты: если пока нет — отдай пустой список
        promo_list = []
        if hasattr(item, "promo_list") and item.promo_list:
            promo_list = [x for x in item.promo_list if x]  # если это массив в JSON
        else:
            # можно собрать из Property.list_details (если это список строк)
            if isinstance(getattr(p, "list_details", None), list):
                promo_list = [str(x) for x in p.list_details][:4]

        items.append({
            # иконка для блока в шаблоне
            "icon": icon,

            # заголовок/описание/цены
            "title": item.title or p.name,
            "description": item.description or (p.summary or p.description[:160] if p.description else ""),
            "old_price": item.old_price,
            "new_price": item.new_price,

            # доп. текст под ценой
            "additional_description": getattr(item, "additional_description", ""),

            # промо-пули (маркированный список)
            "promo_list": promo_list,

            # визуальная тема (если используешь динамику — см. Tailwind замечание ниже)
            "color_theme": color_theme,  # например "red-600" → text-red-600/bg-red-600

            # бейдж «скидка»
            "badge_text": item.badge_text or "SALE",
            "badge_percent": item.badge_percent or 10,

            # истечение
            "expires_in_days": expires_in_days,

            # кнопка
            "button_text": "Подробнее",
            "resolve_url": p.get_absolute_url(),
        })

    return items
