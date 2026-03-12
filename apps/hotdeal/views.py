from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from apps.hotdeal.models import HotDealItem

from apps.properties.models import OfficeUnitImage, OfficeUnit  

def hotdeal_partial(request, public_id):
    item = get_object_or_404(HotDealItem, public_id=public_id, is_active=True)
    unit = getattr(item, "content_object", None)

    is_office = isinstance(unit, OfficeUnit)
    images = []
    if is_office and unit:
        # Не полагаемся на related_name — выбираем напрямую по FK
        images = list(OfficeUnitImage.objects.filter(office_unit=unit).order_by("id"))

    prop = unit.property if is_office and hasattr(unit, "property") else None
    description = (
        (getattr(prop, "description", "") or "")
        or (getattr(unit, "description", "") or "")
        or (item.description or "")
    )
    embed_src = ""
    if unit and hasattr(unit, "embed_src"):
        embed_src = unit.embed_src
    elif prop and hasattr(prop, "embed_src"):
        embed_src = prop.embed_src

    return render(request, "hotdeal/detail.html", {
        "item": item,
        "unit": unit,
        "property": prop,
        "images": images,
        "description": description,
        "map_embed_src": embed_src,
    })


def hotdeal_partial_empty(request):
    # Возвращаем пустой HTML, чтобы htmx очистил #hotdeal-detail-area
    return HttpResponse("")
