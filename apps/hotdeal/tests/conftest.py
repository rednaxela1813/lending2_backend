import uuid
from decimal import Decimal
from itertools import count

import pytest
from django.contrib.contenttypes.models import ContentType

from apps.hotdeal.models import HotDealItem
from apps.properties.models import PropertyType, Property, OfficeUnit


@pytest.fixture
def property_type_factory():
    seq = count(1)

    def factory(**overrides):
        idx = next(seq)
        defaults = {
            "name": f"Type {idx}",
            "slug": f"type-{idx}",
        }
        defaults.update(overrides)
        return PropertyType.objects.create(**defaults)

    return factory


@pytest.fixture
def property_factory(property_type_factory):
    seq = count(1)

    def factory(**overrides):
        idx = next(seq)
        prop_type = overrides.pop("type", None) or property_type_factory()
        defaults = {
            "name": overrides.pop("name", f"Property {idx}"),
            "type": prop_type,
            "description": overrides.pop("description", "Office with a view"),
            "summary": overrides.pop("summary", "Sunny office"),
            "location": overrides.pop("location", "Bratislava"),
            "iframe": overrides.pop("iframe", ""),
        }
        defaults.update(overrides)
        return Property.objects.create(**defaults)

    return factory


@pytest.fixture
def office_unit_factory(property_factory):
    seq = count(1)

    def factory(**overrides):
        prop = overrides.pop("property", None) or property_factory()
        idx = next(seq)
        defaults = {
            "property": prop,
            "floor": overrides.pop("floor", 1),
            "unit_number": overrides.pop("unit_number", f"{idx:03}"),
            "area_sqm": overrides.pop("area_sqm", 48.5),
            "price_per_month": overrides.pop("price_per_month", Decimal("990.00")),
            "description": overrides.pop("description", "Spacious light office"),
        }
        defaults.update(overrides)
        return OfficeUnit.objects.create(**defaults)

    return factory


@pytest.fixture
def hotdeal_item_factory(property_factory):
    def factory(*, content_object=None, **overrides):
        content_object = content_object or property_factory()
        ct = ContentType.objects.get_for_model(content_object.__class__)
        defaults = {
            "content_type": ct,
            "object_id": content_object.pk,
            "title": overrides.pop("title", f"Deal for {content_object.name}"),
        }
        defaults.update(overrides)
        return HotDealItem.objects.create(**defaults)

    return factory
