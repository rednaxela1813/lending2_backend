import pytest
from rest_framework.test import APIClient
from csm.models import SiteTheme
from django.urls import reverse


@pytest.mark.django_db
def test_site_theme_model_str():
    theme = SiteTheme.objects.create(name="Light Theme")
    assert str(theme) == "Light Theme"
    
@pytest.mark.django_db
def test_get_active_theme():
    client = APIClient()
    theme = SiteTheme.objects.create(
        name="Dark Theme",
        primary_color="#000000",
        secondary_color="#111111",
        background_color="#222222",
        text_color="#ffffff",
        is_active=True
    )
    
    url = reverse("active-theme")
    response = client.get(url)
    
    assert response.status_code == 200
    assert response.data['primary_color'] == "#000000"
    assert response.data['secondary_color'] == "#111111"
    assert response.data['background_color'] == "#222222"
    assert response.data['text_color'] == "#ffffff"
    assert response.data['name'] == "Dark Theme"
    assert response.data['is_active'] is True

@pytest.mark.django_db
def test_get_theme_when_none_active():
    client = APIClient()
    SiteTheme.objects.create(name="Inactive Theme", is_active=False)
    
    url = reverse("active-theme")
    response = client.get(url)

    assert response.status_code == 404
    assert response.data['detail'] == "No active theme found"
