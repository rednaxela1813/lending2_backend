# csm/tests/test_service_section.py
import pytest
from django.urls import reverse
from csm.models import ServiceSection
from apps.properties.models import PropertyType

pytestmark = pytest.mark.django_db

def test_service_section_get_list_url_when_type_set():
    ptype = PropertyType.objects.create(name="Offices", slug="office")
    s = ServiceSection.objects.create(title="S1", property_type=ptype)

    url = s.get_list_url()

    # Expect fallback to /offices/?type=office
    assert url == f"{reverse('property_list')}?type=office"

def test_service_section_get_list_url_when_type_none():
    s = ServiceSection.objects.create(title="S2")
    assert s.get_list_url() is None
