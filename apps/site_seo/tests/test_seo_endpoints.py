import pytest
from django.urls import reverse

from apps.properties.models import Property, PropertyType


pytestmark = pytest.mark.django_db


def test_robots_txt_includes_sitemap(client, settings):
    settings.SITE_SEO_ENABLED = True
    settings.SITE_URL = "https://example.com"
    resp = client.get(reverse("site_seo:robots_txt"))
    assert resp.status_code == 200
    assert "Sitemap: https://example.com/sitemap.xml" in resp.content.decode()


def test_sitemap_lists_static_and_property_urls(client, settings):
    settings.SITE_SEO_ENABLED = True
    settings.SITE_URL = "https://example.com"
    ptype = PropertyType.objects.create(slug="office", name="Office")
    prop = Property.objects.create(name="Test", type=ptype)

    resp = client.get(reverse("site_seo:sitemap_xml"))
    assert resp.status_code == 200
    body = resp.content.decode()
    assert reverse("csm:homepage") in body
    assert prop.get_absolute_url() in body
