import hashlib
import pytest
from django.urls import reverse
from django.utils import timezone

from apps.contact_messages.models import ContactMessage


pytestmark = pytest.mark.django_db


def _hash(email: str) -> str:
    return hashlib.sha256(email.strip().lower().encode("utf-8")).hexdigest()


def test_submit_success_creates_message_and_redirects(client, settings):
    url = reverse("contact_messages:submit")
    payload = {
        "first_name": "Alex",
        "last_name": "Kiselev",
        "email": "User@Example.Com",
        "service": "office-space",
        "message": "Hello",
        "gdpr_consent": "on",
    }

    # имитируем прокси-заголовок и реальный REMOTE_ADDR
    resp = client.post(
        url,
        data=payload,
        **{
            "HTTP_X_FORWARDED_FOR": "203.0.113.123",
            "REMOTE_ADDR": "10.0.0.5",
            "HTTP_USER_AGENT": "pytest-agent",
            "HTTP_REFERER": "https://example.com/page",
        },
    )
    assert resp.status_code == 302
    assert resp.url == reverse("contact_messages:success")

    obj = ContactMessage.objects.latest("created_at")
    assert obj.first_name == "Alex"
    assert obj.last_name == "Kiselev"
    assert obj.service == "office-space"
    assert obj.gdpr_consent is True

    # email_hash рассчитан по нормализованному email
    assert obj.email_hash == _hash("User@Example.Com")

    # IP должен быть анонимизирован: 203.0.113.123 -> 203.0.113.0
    assert obj.client_ip == "203.0.113.0"
    assert obj.user_agent == "pytest-agent"
    assert obj.referrer == "https://example.com/page"


def test_submit_requires_gdpr_consent(client):
    url = reverse("contact_messages:submit")
    resp = client.post(
        url,
        data={
            "first_name": "No",
            "last_name": "Consent",
            "email": "n@example.com",
            "service": "office-space",
            "message": "no consent",
            # без gdpr_consent
        },
    )
    assert resp.status_code == 400  # HttpResponseBadRequest
    assert ContactMessage.objects.count() == 0


@pytest.mark.parametrize("missing_field", ["first_name", "last_name", "email", "service"])
def test_submit_missing_required_fields(client, missing_field):
    url = reverse("contact_messages:submit")
    base = {
        "first_name": "A",
        "last_name": "B",
        "email": "e@example.com",
        "service": "office-space",
        "gdpr_consent": "on",
    }
    base.pop(missing_field)
    resp = client.post(url, data=base)
    assert resp.status_code == 400
    assert ContactMessage.objects.count() == 0


def test_ipv6_anonymization(client):
    url = reverse("contact_messages:submit")
    resp = client.post(
        url,
        data={
            "first_name": "V6",
            "last_name": "User",
            "email": "v6@example.com",
            "service": "office-space",
            "gdpr_consent": "on",
        },
        **{"HTTP_X_FORWARDED_FOR": "2001:db8:abcd:0012:0000:0000:0000:0001"},
    )
    assert resp.status_code == 302
    obj = ContactMessage.objects.latest("created_at")
    # ожидаем обрезку до /64 сети (например, 2001:db8:abcd:12::)
    assert obj.client_ip.startswith("2001:db8:abcd:12:")
