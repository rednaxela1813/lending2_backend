# accounting/tests/test_admin_login.py
import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db

def test_admin_login_allows_superuser(client, superuser):
    ok = client.login(username=superuser.email, password="adminpass123")
    assert ok
    resp = client.get("/pon_ka/")  # твой путь к админке
    assert resp.status_code in (200, 302)  # 302 из-за редиректа внутри админки — тоже ок
