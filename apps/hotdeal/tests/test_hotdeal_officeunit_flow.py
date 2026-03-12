from decimal import Decimal

import pytest
from django.contrib.contenttypes.models import ContentType

from apps.hotdeal.models import HotDealItem
from apps.properties.models.mixins import Availability


pytestmark = pytest.mark.django_db


def _fetch_hotdeal(unit):
    ct = ContentType.objects.get_for_model(unit.__class__)
    return HotDealItem.objects.get(content_type=ct, object_id=unit.pk)


def test_hotdeal_created_for_available_unit(office_unit_factory):
    unit = office_unit_factory()
    item = _fetch_hotdeal(unit)
    assert item.is_active is True
    assert item.title == str(unit)


def test_hotdeal_defaults_populated_from_unit(office_unit_factory):
    unit = office_unit_factory(area_sqm=123.0, price_per_month=Decimal("1500.00"))
    item = _fetch_hotdeal(unit)
    assert item.new_price == Decimal("1500.00")
    assert item.additional_description == "123 m²"
    assert item.badge_text == "SALE"


def test_hotdeal_deactivates_when_unit_not_available_anymore(office_unit_factory):
    unit = office_unit_factory()
    item = _fetch_hotdeal(unit)
    unit.availability = Availability.OCCUPIED
    unit.save()
    item.refresh_from_db()
    assert item.is_active is False


def test_hotdeal_reactivates_when_unit_becomes_available_again(office_unit_factory):
    unit = office_unit_factory()
    item = _fetch_hotdeal(unit)
    unit.availability = Availability.OCCUPIED
    unit.save()
    unit.availability = Availability.AVAILABLE
    unit.save()
    item.refresh_from_db()
    assert item.is_active is True


def test_hotdeal_deleted_when_unit_removed(office_unit_factory):
    unit = office_unit_factory()
    _fetch_hotdeal(unit)
    unit.delete()
    ct = ContentType.objects.get_for_model(unit.__class__)
    assert HotDealItem.objects.filter(content_type=ct, object_id=unit.pk).count() == 0
