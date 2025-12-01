import pytest
from django.core import mail
from django.utils import timezone

from apps.contact_messages.models import ContactMessage
from apps.site_email.services import send_contact_message_email


pytestmark = pytest.mark.django_db


def _create_message(**overrides):
    base = {
        "first_name": "Alex",
        "last_name": "Tester",
        "email": "alex@example.com",
        "service": "office-space",
        "message": "Please call me back.",
        "gdpr_consent": True,
        "consent_at": timezone.now(),
        "consent_version": "v1",
        "client_ip": "203.0.113.0",
        "user_agent": "pytest-agent",
        "referrer": "https://example.com",
        "source_path": "/contact",
    }
    base.update(overrides)
    return ContactMessage.objects.create(**base)


def test_send_contact_message_email_sends(settings):
    settings.SITE_EMAIL_RECIPIENTS = ["owner@example.com"]
    settings.DEFAULT_FROM_EMAIL = "noreply@example.com"

    message = _create_message()

    sent = send_contact_message_email(message)
    assert sent is True
    assert len(mail.outbox) == 1

    email = mail.outbox[0]
    assert email.to == ["owner@example.com"]
    assert email.from_email == "noreply@example.com"
    assert "Alex Tester" in email.subject
    assert "Office Space" in email.subject  # humanized label from slug
    assert "Please call me back." in email.body
    assert "Client IP" in email.body


def test_send_contact_message_email_skips_without_recipients(settings):
    settings.SITE_EMAIL_RECIPIENTS = []
    message = _create_message()

    sent = send_contact_message_email(message)
    assert sent is False
    assert mail.outbox == []


def test_send_contact_message_email_handles_exception(monkeypatch, settings):
    settings.SITE_EMAIL_RECIPIENTS = ["owner@example.com"]

    def boom(self, fail_silently=False):
        raise RuntimeError("SMTP down")

    monkeypatch.setattr("apps.site_email.services.EmailMultiAlternatives.send", boom)

    message = _create_message()

    sent = send_contact_message_email(message)
    assert sent is False
    assert mail.outbox == []
