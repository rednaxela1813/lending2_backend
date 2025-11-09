import uuid

import pytest

from apps.hotdeal.context import build_hot_deal_items
from csm.models import Icon


pytestmark = pytest.mark.django_db


def test_builder_returns_icon_from_item(hotdeal_item_factory):
    icon = Icon.objects.create(
        key=f"icon-{uuid.uuid4().hex[:6]}",
        label="Star",
        svg_inline="<svg>ITEM</svg>",
    )
    hotdeal_item_factory(icon=icon, promo_1="Wi-Fi", description="Great deal")

    payload = build_hot_deal_items()
    assert len(payload) == 1
    entry = payload[0]
    assert entry["icon"] == {"svg_inline": "<svg>ITEM</svg>", "label": "Star"}
    assert entry["promo_list"] == ["Wi-Fi"]
    assert entry["description"] == "Great deal"


def test_builder_skips_inactive_items(hotdeal_item_factory):
    hotdeal_item_factory(title="Active deal")
    hotdeal_item_factory(title="Hidden deal", is_active=False)

    payload = build_hot_deal_items()
    assert [item["title"] for item in payload] == ["Active deal"]
