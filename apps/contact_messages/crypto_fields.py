# apps/contact_messages/crypto_fields.py
from django.conf import settings
from django.core import checks
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.encoding import force_str
from cryptography.fernet import Fernet, MultiFernet, InvalidToken


def _get_fernet():
    keys = getattr(settings, "FERNET_KEYS", None)
    if not keys:
        raise ImproperlyConfigured("FERNET_KEYS is not configured in settings.")
    fernets = [Fernet(force_str(k).encode()) for k in keys]
    # MultiFernet расшифрует любым ключом, зашифрует первым
    return MultiFernet(fernets)

_F = None
def fernet():
    global _F
    if _F is None:
        _F = _get_fernet()
    return _F


class EncryptedMixin:
    """
    Миксин для шифрования строковых значений в БД.
    Хранит токен Fernet (base64 urlsafe), а в приложении отдаёт обычную строку.
    """

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # Никаких доп. аргументов — схема БД остаётся обычной
        return name, path, args, kwargs

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        # проверим конфиг ключей на старте
        try:
            fernet()
        except ImproperlyConfigured as e:
            errors.append(
                checks.Error(str(e), id="contact_messages.E001")
            )
        return errors

    def get_prep_value(self, value):
        """
        Преобразование Python -> значение для БД.
        Шифруем непустые строки.
        """
        if value is None or value == "":
            return value
        if not isinstance(value, (str, bytes)):
            value = str(value)
        if isinstance(value, str):
            value = value.encode("utf-8")
        token = fernet().encrypt(value)  # bytes
        return token.decode("ascii")     # храним строкой

    def from_db_value(self, value, expression, connection):
        """
        Преобразование из БД в Python (работает при select).
        """
        if value is None or value == "":
            return value
        if isinstance(value, str):
            value = value.encode("ascii")
        try:
            plain = fernet().decrypt(value)
            return plain.decode("utf-8")
        except InvalidToken:
            # если по какой-то причине в колонке уже лежит открытый текст (на ранних этапах),
            # просто вернём как есть
            try:
                return value.decode("utf-8")
            except Exception:
                return value

    def to_python(self, value):
        """
        Вызывается валидатором/формами; если пришёл токен — расшифруем,
        если обычная строка — оставим.
        """
        if value is None or value == "":
            return value
        # Пробуем распознать токен Fernet (base64 urlsafe)
        if isinstance(value, str):
            try:
                # Попытка расшифровать — если не токен, упадёт в InvalidToken
                return fernet().decrypt(value.encode("ascii")).decode("utf-8")
            except Exception:
                return value
        if isinstance(value, bytes):
            try:
                return fernet().decrypt(value).decode("utf-8")
            except Exception:
                return value
        return str(value)


class EncryptedTextField(EncryptedMixin, models.TextField):
    description = "TextField, encrypted at rest using Fernet"


class EncryptedEmailField(EncryptedMixin, models.EmailField):
    description = "EmailField, encrypted at rest using Fernet"
