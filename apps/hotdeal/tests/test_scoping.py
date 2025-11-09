from datetime import date, timedelta

import pytest

from apps.hotdeal.context import build_hot_deal_items


pytestmark = pytest.mark.django_db


def test_builder_returns_items_sorted_by_id(hotdeal_item_factory):
    first = hotdeal_item_factory(title="First deal")
    second = hotdeal_item_factory(title="Second deal")

    titles = [item["title"] for item in build_hot_deal_items()]
    assert titles == [first.title, second.title]


def test_builder_computes_expires_in_days(hotdeal_item_factory):
    hotdeal_item_factory(date_expiry=date.today() + timedelta(days=3))
    entry = build_hot_deal_items()[0]
    assert entry["expires_in_days"] == 3


def test_builder_falls_back_to_defaults_when_fields_missing(hotdeal_item_factory):
    hotdeal_item_factory(badge_text="", badge_percent=None, button_text="")
    entry = build_hot_deal_items()[0]
    assert entry["badge_text"] == "SALE"
    assert entry["badge_percent"] == 10
    assert entry["button_text"] == "Zanechajte žiadosť"
    assert entry["resolve_url"] == "#contact"
