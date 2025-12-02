import pytest
from django.urls import reverse

from cookie_consent.conf import settings as cookie_settings
from cookie_consent.models import Cookie, CookieGroup
from cookie_consent.util import parse_cookie_str


pytestmark = pytest.mark.django_db


def _make_group(varname: str, *, required: bool = False) -> CookieGroup:
    group = CookieGroup.objects.create(
        varname=varname,
        name=varname.title(),
        is_required=required,
    )
    Cookie.objects.create(cookiegroup=group, name=f"{varname}_cookie", path="/")
    return group


def _parse_consent_cookie(response):
    cookie = response.cookies[cookie_settings.COOKIE_CONSENT_NAME]
    return parse_cookie_str(cookie.value)


def test_accept_all_marks_every_group_as_accepted(client):
    essential = _make_group("necessary", required=True)
    analytics = _make_group("analytics")

    resp = client.post(reverse("cookie_consent_accept_all"))
    assert resp.status_code == 302
    assert cookie_settings.COOKIE_CONSENT_NAME in resp.cookies

    state = _parse_consent_cookie(resp)
    assert state[essential.varname] == essential.get_version()
    assert state[analytics.varname] == analytics.get_version()


def test_decline_all_marks_non_necessary_groups_as_declined(client):
    essential = _make_group("necessary", required=True)
    analytics = _make_group("analytics")

    resp = client.post(reverse("cookie_consent_decline_all"))
    assert resp.status_code == 302
    assert cookie_settings.COOKIE_CONSENT_NAME in resp.cookies

    state = _parse_consent_cookie(resp)
    assert state[essential.varname] == essential.get_version()
    assert state[analytics.varname] == cookie_settings.COOKIE_CONSENT_DECLINE
