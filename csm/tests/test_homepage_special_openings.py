import datetime

import pytest
from django.urls import reverse
from django.utils import timezone

from apps.company.models import CompanyInfo, SpecialOpening


pytestmark = pytest.mark.django_db


def _ctx(response):
    """Django test client returns a list of contexts for TemplateResponses."""
    return response.context[-1] if isinstance(response.context, list) else response.context


def _company():
    return CompanyInfo.objects.create(
        name="Test Co",
        ico="1",
        dic="2",
        address="Addr",
        phone="123",
        email="test@example.com",
    )


def test_homepage_uses_future_specials_and_sets_next_closed(monkeypatch, client):
    today = datetime.date(2025, 12, 1)
    monkeypatch.setattr(timezone, "localdate", lambda: today)

    company = _company()
    past_closed = SpecialOpening.objects.create(company=company, date=datetime.date(2025, 11, 2), is_closed=True)
    next_closed = SpecialOpening.objects.create(company=company, date=datetime.date(2025, 12, 2), is_closed=True, note="Holiday")
    SpecialOpening.objects.create(
        company=company,
        date=datetime.date(2025, 12, 3),
        is_closed=False,
        start_time=datetime.time(10, 0),
        end_time=datetime.time(14, 0),
    )

    resp = client.get(reverse("csm:homepage"))
    assert resp.status_code == 200
    ctx = _ctx(resp)

    dates = list(ctx["upcoming_specials"].values_list("date", flat=True))
    assert past_closed.date not in dates  # outdated date removed
    assert dates[0] == next_closed.date  # soonest upcoming first
    assert ctx["next_closed_weekday"] == next_closed.date.weekday()


def test_homepage_no_future_closed(monkeypatch, client):
    today = datetime.date(2025, 12, 10)
    monkeypatch.setattr(timezone, "localdate", lambda: today)

    company = _company()
    SpecialOpening.objects.create(
        company=company,
        date=datetime.date(2025, 12, 12),
        is_closed=False,
        start_time=datetime.time(9, 0),
        end_time=datetime.time(11, 0),
    )

    resp = client.get(reverse("csm:homepage"))
    assert resp.status_code == 200
    ctx = _ctx(resp)

    assert ctx["upcoming_specials"].count() == 1
    assert ctx["next_closed_weekday"] is None  # nothing closed ahead
