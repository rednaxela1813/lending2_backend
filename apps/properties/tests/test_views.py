import pytest
from django.urls import reverse

from apps.properties.models import PropertyType, Property


pytestmark = pytest.mark.django_db


def test_property_list_filters_by_type(client):
    t_office = PropertyType.objects.create(name="Office", slug="offices")
    t_billboard = PropertyType.objects.create(name="Billboard", slug="billboards")
    p_office = Property.objects.create(name="Office A", type=t_office)
    p_billboard = Property.objects.create(name="Billboard B", type=t_billboard)

    url = reverse("property_list") + "?type=billboards"
    resp = client.get(url)
    assert resp.status_code == 200
    properties = list(resp.context["properties"])
    assert properties == [p_billboard]

    # default should be offices
    resp_default = client.get(reverse("property_list"))
    props_default = list(resp_default.context["properties"])
    assert props_default == [p_office]
