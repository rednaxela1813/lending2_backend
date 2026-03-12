import logging
from typing import Iterable, Sequence

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


logger = logging.getLogger(__name__)


_SERVICE_LABELS = {
    "office-space": "Office Space",
    "office_space": "Office Space",
    "billboard": "Billboard Advertising",
    "legal-address": "Legal Address",
    "legal_address": "Legal Address",
    "multiple": "Multiple Services",
}


def _parse_recipients(raw: str | Sequence[str] | None) -> list[str]:
    """
    Normalize recipients list that may come as comma-separated string
    or a sequence. Empty/None -> [].
    """
    if not raw:
        return []
    if isinstance(raw, str):
        return [item.strip() for item in raw.split(",") if item.strip()]
    return [item.strip() for item in raw if item and str(item).strip()]


def _service_label(value: str | None) -> str:
    if not value:
        return "Contact"
    if value in _SERVICE_LABELS:
        return _SERVICE_LABELS[value]
    normalized = value.replace("_", " ").replace("-", " ").strip()
    return normalized.title() if normalized else "Contact"


def _get_recipients() -> list[str]:
    recipients = getattr(settings, "SITE_EMAIL_RECIPIENTS", [])
    return _parse_recipients(recipients)


def send_contact_message_email(message) -> bool:
    """
    Send an email to the configured recipients with details
    of a contact form submission.

    Returns True if the email was sent, False if skipped or failed.
    Never raises to keep the form UX uninterrupted.
    """
    recipients = _get_recipients()
    if not recipients:
        logger.info("site_email: no SITE_EMAIL_RECIPIENTS configured; skipping send.")
        return False

    service_label = _service_label(getattr(message, "service", ""))
    subject = f"[Contact] {service_label} – {message.first_name} {message.last_name}"

    context = {
        "message": message,
        "service_label": service_label,
        "site_name": getattr(settings, "SITE_NAME", "Website"),
    }
    body = render_to_string("site_email/contact_message.txt", context)

    email = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
        to=recipients,
        reply_to=[getattr(message, "email", "")] if getattr(message, "email", "") else None,
    )

    try:
        email.send(fail_silently=False)
        return True
    except Exception:
        logger.exception("site_email: failed to send contact message email")
        return False

