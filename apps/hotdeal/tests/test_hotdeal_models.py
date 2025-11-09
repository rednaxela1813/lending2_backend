from datetime import timedelta

import pytest
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from django.utils import timezone

from apps.hotdeal.models import HotDealItem, HotDealSection


pytestmark = pytest.mark.django_db


def test_expires_in_days_none_when_expiry_missing(hotdeal_item_factory):
    item = hotdeal_item_factory(date_expiry=None)
    assert item.expires_in_days is None


def test_expires_in_days_positive_value(hotdeal_item_factory):
    item = hotdeal_item_factory(date_expiry=timezone.now().date() + timedelta(days=5))
    assert item.expires_in_days == 5


def test_promo_list_filters_empty_values(hotdeal_item_factory):
    item = hotdeal_item_factory(
        promo_1="Wi-Fi",
        promo_2="",
        promo_3="Parking",
        promo_4="",
    )
    assert item.promo_list == ["Wi-Fi", "Parking"]


def test_hotdealitem_str_returns_title(hotdeal_item_factory):
    item = hotdeal_item_factory(title="Sky Office Promo")
    assert str(item) == "Sky Office Promo"


def test_unique_constraint_per_content_object(property_factory):
    prop = property_factory()
    ct = ContentType.objects.get_for_model(prop.__class__)
    HotDealItem.objects.create(content_type=ct, object_id=prop.pk, title="Deal A")
    with pytest.raises(IntegrityError):
        HotDealItem.objects.create(content_type=ct, object_id=prop.pk, title="Deal B")


def test_hotdealsection_str():
    section = HotDealSection.objects.create(title="Limited Offers")
    assert str(section) == "Limited Offers"
