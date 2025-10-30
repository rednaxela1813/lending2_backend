import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db

def test_dashboard_requires_login(client):
    url = reverse("dashboard:home")
    resp = client.get(url, follow=False)
    assert resp.status_code == 302
    assert "/accounts/login/" in resp["Location"]

def test_dashboard_renders_for_authenticated(logged_in_client, user):
    resp = logged_in_client.get(reverse("dashboard:home"))
    assert resp.status_code == 200
    assert user.email.encode() in resp.content or (user.full_name or "").encode() in resp.content

def test_login_redirects_to_dashboard(client, user, settings):
    settings.LOGIN_REDIRECT_URL = "dashboard:home"
    resp = client.post(reverse("login"), {"username": user.email, "password": "testpass123"})
    assert resp.status_code == 302
    assert reverse("dashboard:home") in resp["Location"]
