import hashlib
import pytest
from datetime import timedelta
from django.core.management import call_command
from django.utils import timezone

from apps.contact_messages.models import ContactMessage


pytestmark = pytest.mark.django_db


def make_msg(age_days: int, **kwargs):
    dt = timezone.now() - timedelta(days=age_days)
    obj = ContactMessage.objects.create(
        first_name=kwargs.get("first_name", "Old"),
        last_name=kwargs.get("last_name", "User"),
        email=kwargs.get("email", "old@example.com"),
        service=kwargs.get("service", "office-space"),
        message=kwargs.get("message", "hi"),
        gdpr_consent=True,
    )
    # принудительно сдвигаем created_at назад (если auto_now_add)
    ContactMessage.objects.filter(pk=obj.pk).update(created_at=dt)
    return ContactMessage.objects.get(pk=obj.pk)


def test_purge_dry_run_does_not_delete(capsys):
    old = make_msg(age_days=1000)  # ~33 месяца
    recent = make_msg(age_days=10)

    call_command("purge_old_messages", months=24, dry_run=True)
    captured = capsys.readouterr()
    assert "DRY-RUN" in captured.out

    # ничего не удалено
    assert ContactMessage.objects.filter(pk=old.pk).exists()
    assert ContactMessage.objects.filter(pk=recent.pk).exists()


def test_purge_delete_old_only():
    old = make_msg(age_days=800)   # > 24 месяцев
    recent = make_msg(age_days=10)

    call_command("purge_old_messages", months=24)
    # старый удалён, новый остался
    assert not ContactMessage.objects.filter(pk=old.pk).exists()
    assert ContactMessage.objects.filter(pk=recent.pk).exists()


def test_purge_anonymize_old_records():
    old = make_msg(age_days=800, email="pii@example.com", message="secret")
    recent = make_msg(age_days=10, email="stay@example.com", message="keep")

    call_command("purge_old_messages", months=24, anonymize=True)

    old_ref = ContactMessage.objects.get(pk=old.pk)
    # PII очищены
    assert old_ref.first_name == ""
    assert old_ref.last_name == ""
    assert old_ref.email == ""  # поле расшифровывается в пустую строку
    assert old_ref.message == ""
    assert old_ref.gdpr_consent is False

    # недавняя запись нетронута
    assert ContactMessage.objects.get(pk=recent.pk).email != ""
