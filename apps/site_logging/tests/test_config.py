import logging
import logging.config

import pytest
from django.core import mail
from django.utils.log import AdminEmailHandler

from apps.site_logging.config import get_logging_config


pytestmark = pytest.mark.django_db


def test_config_includes_mail_handler_when_admins(settings):
    settings.ADMINS = [("Owner", "owner@example.com")]
    cfg = get_logging_config(debug=False)

    assert "mail_admins" in cfg["handlers"]
    assert "mail_admins" in cfg["loggers"]["django.request"]["handlers"]
    assert "mail_admins" in cfg["root"]["handlers"]


def test_config_skips_mail_handler_without_admins(settings):
    settings.ADMINS = []
    cfg = get_logging_config(debug=False)
    assert "mail_admins" not in cfg["handlers"]
    assert cfg["root"]["handlers"] == ["console"]


def test_admin_email_handler_sends_email(settings):
    settings.ADMINS = [("Owner", "owner@example.com")]
    settings.SERVER_EMAIL = "server@example.com"
    handler = AdminEmailHandler(include_html=True)

    record = logging.LogRecord(
        name="django.request",
        level=logging.ERROR,
        pathname=__file__,
        lineno=42,
        msg="Boom!",
        args=(),
        exc_info=None,
    )

    handler.emit(record)

    assert len(mail.outbox) == 1
    email = mail.outbox[0]
    assert email.to == ["owner@example.com"]
    assert "Boom" in email.subject or "Boom" in email.body
