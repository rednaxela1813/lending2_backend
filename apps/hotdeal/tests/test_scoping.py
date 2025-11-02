import pytest
from accounting.models import Company
from apps.hotdeal.models import HotDealItem, HotDealSection
from apps.properties.models import Property, PropertyType



pytestmark = pytest.mark.django_db

@pytest.fixture
def ptype():
    return PropertyType.objects.create(name="Office", icon_svg="<svg>PT</svg>")

@pytest.fixture
def prop_c1(ptype):
    return Property.objects.create(name="P1", type=ptype)

@pytest.fixture
def prop_c2(ptype):
    return Property.objects.create(name="P2", type=ptype)

@pytest.fixture
def section_active():
    return HotDealSection.objects.create(name="Main", is_active=True)

def test_hotdeal_scoped_by_company(section_active, prop_c1, prop_c2):
    from apps.hotdeal.context import build_hot_deal_items
    c1 = Company.objects.create(name="Zavodsky", slug="zv")
    c2 = Company.objects.create(name="Other", slug="ot")

    HotDealItem.objects.create(section=section_active, property=prop_c1, title="Deal C1", is_active=True, company=c1)
    HotDealItem.objects.create(section=section_active, property=prop_c2, title="Deal C2", is_active=True, company=c2)
    # глобальное (видно всем)
    HotDealItem.objects.create(section=section_active, property=prop_c1, title="Global Deal", is_active=True, company=None)

    items_c1 = build_hot_deal_items(company=c1)
    titles_c1 = {i["title"] for i in items_c1}
    assert "Deal C1" in titles_c1 and "Global Deal" in titles_c1 and "Deal C2" not in titles_c1

    items_c2 = build_hot_deal_items(company=c2)
    titles_c2 = {i["title"] for i in items_c2}
    assert "Deal C2" in titles_c2 and "Global Deal" in titles_c2 and "Deal C1" not in titles_c2
