import hashlib
import pytest
from django.db import connection

from apps.contact_messages.models import ContactMessage


pytestmark = pytest.mark.django_db


def _hash(email: str) -> str:
    return hashlib.sha256(email.strip().lower().encode("utf-8")).hexdigest()


def test_email_and_message_encrypted_at_rest(settings):
    # создаём запись обычным способом
    obj = ContactMessage.objects.create(
        first_name="Enc",
        last_name="Test",
        email="secret@example.com",
        service="office-space",
        message="Sensitive message here",
        gdpr_consent=True,
    )

    # ORM отдаёт расшифрованные значения
    obj_refetched = ContactMessage.objects.get(pk=obj.pk)
    assert obj_refetched.email == "secret@example.com"
    assert obj_refetched.message == "Sensitive message here"

    # но в БД хранится зашифрованный токен (не равен открытым строкам)
    table = ContactMessage._meta.db_table  # ← динамическое имя таблицы
    with connection.cursor() as cur:
        cur.execute(
            f'SELECT email, message FROM "{table}" WHERE id=%s',
            [str(obj.pk)],
        )
        raw_email, raw_message = cur.fetchone()

    assert isinstance(raw_email, str)
    assert isinstance(raw_message, str)
    assert raw_email != "secret@example.com"
    assert raw_message != "Sensitive message here"
    # грубая проверка: ciphertext не должен содержать «@example.com»
    assert "@example.com" not in raw_email

    # email_hash заполнен корректно
    assert obj_refetched.email_hash == _hash("secret@example.com")
