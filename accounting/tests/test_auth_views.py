import pytest
from django.urls import reverse
from django.test import override_settings

pytestmark = pytest.mark.django_db


def test_login_page_renders(client):
    resp = client.get(reverse("login"))
    assert resp.status_code == 200
    assert b'name="username"' in resp.content
    assert b'name="password"' in resp.content


@override_settings(LOGIN_REDIRECT_URL="/pon_ka/")  # перенаправляем в админку
def test_login_success_redirects_to_setting(client, user):
    resp = client.post(
        reverse("login"),
        {"username": user.email, "password": "testpass123"},
        follow=False,
    )
    assert resp.status_code == 302
    assert resp["Location"].endswith("/pon_ka/")


@override_settings(LOGIN_REDIRECT_URL="/pon_ka/")
def test_login_respects_next_param(client, user):
    login_url = reverse("login") + "?next=/kontakt/"
    resp = client.post(
        login_url,
        {"username": user.email, "password": "testpass123"},
        follow=False,
    )
    assert resp.status_code == 302
    assert resp["Location"].endswith("/kontakt/")


def test_login_invalid_credentials(client):
    resp = client.post(reverse("login"), {"username": "wrong@example.com", "password": "bad"})
    assert resp.status_code == 200
    assert resp.wsgi_request.user.is_authenticated is False


def test_logout_makes_user_anonymous(logged_in_client):
    resp = logged_in_client.post(reverse("logout"), follow=True)
    assert resp.status_code == 200
    assert resp.wsgi_request.user.is_authenticated is False



def test_password_change_flow(logged_in_client, user):
    get_resp = logged_in_client.get(reverse("password_change"))
    assert get_resp.status_code == 200

    post_resp = logged_in_client.post(
        reverse("password_change"),
        {
            "old_password": "testpass123",
            "new_password1": "newpass5678",
            "new_password2": "newpass5678",
        },
        follow=True,
    )
    assert post_resp.status_code == 200

    # новый пароль работает
    logged_in_client.logout()
    ok = logged_in_client.login(username=user.email, password="newpass5678")
    assert ok is True


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
def test_password_reset_sends_email(client, user):
    resp = client.post(reverse("password_reset"), {"email": user.email})
    assert resp.status_code in (302, 303)

    from django.core import mail
    assert len(mail.outbox) == 1
    assert user.email in mail.outbox[0].to
    assert "password reset" in mail.outbox[0].subject.lower()
