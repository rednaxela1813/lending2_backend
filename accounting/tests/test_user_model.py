# accounting/tests/test_user_model.py
import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.urls import reverse

pytestmark = pytest.mark.django_db

def test_settings_use_custom_user_model():
    User = get_user_model()
    assert User.__name__ == "CustomUser"
    assert User._meta.app_label == "accounting"

def test_create_user_minimal_ok():
    User = get_user_model()
    u = User.objects.create_user(email="user@example.com", password="pass1234")
    assert u.pk is not None
    assert u.email == "user@example.com"
    assert u.is_active is True
    assert u.is_staff is False
    assert u.password != "pass1234"
    assert u.check_password("pass1234")

def test_email_normalized_on_create_user():
    User = get_user_model()
    u = User.objects.create_user(email="USER@EXAMPLE.COM", password="x")
    # BaseUserManager.normalize_email — домен в нижний регистр, локальная часть без изменений
    assert u.email == "USER@example.com"

def test_create_user_requires_email():
    User = get_user_model()
    with pytest.raises(ValueError, match="Email должен быть указан"):
        User.objects.create_user(email=None, password="x")
    with pytest.raises(ValueError, match="Email должен быть указан"):
        User.objects.create_user(email="", password="x")

def test_email_unique_constraint():
    User = get_user_model()
    User.objects.create_user(email="dup@example.com", password="x")
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            User.objects.create_user(email="dup@example.com", password="y")

def test_str_returns_email():
    User = get_user_model()
    u = User.objects.create_user(email="me@example.com", password="x")
    assert str(u) == "me@example.com"

def test_create_superuser_ok_and_flags_forced_true():
    User = get_user_model()
    su = User.objects.create_superuser(email="admin@example.com", password="root")
    assert su.is_staff is True
    assert su.is_superuser is True
    assert su.check_password("root")

def test_create_superuser_requires_is_staff_true():
    User = get_user_model()
    with pytest.raises(ValueError, match="is_staff=True"):
        User.objects.create_superuser(email="a@example.com", password="x", is_staff=False)

def test_create_superuser_requires_is_superuser_true():
    User = get_user_model()
    with pytest.raises(ValueError, match="is_superuser=True"):
        User.objects.create_superuser(email="b@example.com", password="x", is_superuser=False)



def test_can_login_with_email(client):
    User = get_user_model()
    u = User.objects.create_user(email="login@example.com", password="pass1234")
    resp = client.post(reverse("login"), {"username": u.email, "password": "pass1234"})
    # При успешном логине LoginView делает 302
    assert resp.status_code == 302
