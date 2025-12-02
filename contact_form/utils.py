from django.conf import settings
from django.core.mail import EmailMessage, get_connection


def _recipients():
    raw = getattr(settings, "SITE_EMAIL_RECIPIENTS", []) or []
    return [r for r in raw if r]


def send_contact_email(subject, body, reply_to=None):
    """
    Lightweight email sender that respects settings-based SMTP config.
    Falls back to console backend in DEBUG. Skips silently if no recipients.
    """
    recipients = _recipients()
    if not recipients:
        print("ℹ️ No SITE_EMAIL_RECIPIENTS configured; skipping send.")
        return False

    backend = settings.EMAIL_BACKEND
    connection_kwargs = {"timeout": getattr(settings, "EMAIL_TIMEOUT", 10)}

    connection = get_connection(backend=backend, **connection_kwargs)
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None)

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=from_email,
        to=recipients,
        connection=connection,
        reply_to=[reply_to] if reply_to else None,
    )

    try:
        email.send(fail_silently=False)
        print("✅ Email sent.")
        return True
    except Exception as e:
        print("❌ Email send failed:", e)
        return False
