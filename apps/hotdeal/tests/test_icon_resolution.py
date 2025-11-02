import pytest
from accounting.models import Company
from apps.hotdeal.models import HotDealItem, HotDealSection
from apps.properties.models import Property, PropertyType
from csm.models import Icon  # у тебя в csm есть Icon со svg_inline



pytestmark = pytest.mark.django_db

@pytest.fixture
def section_active():
    return HotDealSection.objects.create(name="Main", is_active=True, order=1)

def test_icon_priority_item_icon_over_property_type(section_active):
    from apps.hotdeal.context import build_hot_deal_items
    c = Company.objects.create(name="Z", slug="z")

    ptype = PropertyType.objects.create(name="Office", icon_svg="<svg>TYPE</svg>")
    prop = Property.objects.create(name="HQ", type=ptype)

    item_icon = Icon.objects.create(svg_inline="<svg>ITEM</svg>")
    HotDealItem.objects.create(
        section=section_active, property=prop, title="Deal", is_active=True, company=c, icon=item_icon
    )

    items = build_hot_deal_items(company=c)
    assert items[0]["icon"]["svg_inline"] == "<svg>ITEM</svg>"

def test_icon_fallback_to_property_type(section_active):
    from apps.hotdeal.context import build_hot_deal_items
    c = Company.objects.create(name="Z", slug="z")

    ptype = PropertyType.objects.create(name="Office", icon_svg="<svg>TYPE</svg>")
    prop = Property.objects.create(name="HQ", type=ptype)

    HotDealItem.objects.create(
        section=section_active, property=prop, title="Deal", is_active=True, company=c, icon=None
    )

    items = build_hot_deal_items(company=c)
    assert items[0]["icon"]["svg_inline"] == "<svg>TYPE</svg>"
