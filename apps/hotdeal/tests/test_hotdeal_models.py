import pytest
from datetime import date, timedelta
from apps.hotdeal.models import HotDealItem, HotDealSection

pytestmark = pytest.mark.django_db


def test_hotdealitem_expires_in_days_none_when_no_date(property_factory, section_factory):
    p = property_factory()
    s = section_factory()
    item = HotDealItem.objects.create(section=s, property=p, title="X")
    assert item.expires_in_days is None


def test_hotdealitem_expires_in_days_positive(property_factory, section_factory):
    p = property_factory()
    s = section_factory()
    tomorrow = date.today() + timedelta(days=1)
    item = HotDealItem.objects.create(section=s, property=p, title="X", date_expiry=tomorrow)
    # допускаем 1 день (± часовые пояса не влияют, т.к. date vs date)
    assert item.expires_in_days == 1


def test_hotdealitem_str_uses_title(property_factory, section_factory):
    p = property_factory(name="Office A")
    s = section_factory()
    item = HotDealItem.objects.create(section=s, property=p, title="Super Deal")
    assert str(item) == "Super Deal"


def test_hotdealitem_str_fallbacks_to_property(property_factory, section_factory):
    p = property_factory(name="Office B")
    s = section_factory()
    item = HotDealItem.objects.create(section=s, property=p, title="")
    assert str(item) == "Office B"
