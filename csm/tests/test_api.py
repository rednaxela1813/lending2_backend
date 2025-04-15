# csm/tests/test_api.py
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from csm.models import HeroSection, HeaderSection, FooterInfo, CompanyInfo, ContactRequest

pytestmark = pytest.mark.django_db

client = APIClient()


def test_hero_section_view():
    hero = HeroSection.objects.create(
        title="Hello",
        subtitle="Sub",
        image="hero_images/test.jpg"
    )
    response = client.get(reverse("hero-section"))
    assert response.status_code == 200
    assert response.data["title"] == "Hello"


def test_header_section_view():
    HeaderSection.objects.create(images="logo/test.png")
    response = client.get(reverse("header-section"))
    assert response.status_code == 200
    assert "logo_text" in response.data


def test_footer_info_view():
    FooterInfo.objects.create(
        about_description="About us",
        contact_email="test@example.com",
        contact_phone="123456789",
        contact_address="Test Street"
    )
    response = client.get(reverse("footer-info"))
    assert response.status_code == 200
    assert "about_title" in response.data


def test_company_info_view():
    CompanyInfo.objects.create(
        name="Test Company",
        address="Somewhere",
        phone="000000000",
        email="test@firm.com"
    )
    response = client.get(reverse("company-info"))
    assert response.status_code == 200
    assert response.data["name"] == "Test Company"


def test_contact_request_view(monkeypatch, settings):
    settings.ALLOWED_ORIGINS = ["http://localhost:5173"]
    settings.TELEGRAM_BOT_TOKEN = "fake-token"
    settings.TELEGRAM_CHAT_ID = "fake-id"

    def fake_post(url, json):
        class R:
            def raise_for_status(self): pass
        return R()

    monkeypatch.setattr("requests.post", fake_post)

    headers = {"HTTP_ORIGIN": "http://localhost:5173"}
    payload = {
        "name": "Alex",
        "contact": "alex@example.com",
        "message": "Hello"
    }
    response = client.post(reverse("contact-form"), payload, **headers)
    assert response.status_code == 200
    assert response.json()["success"] == "Message sent"
