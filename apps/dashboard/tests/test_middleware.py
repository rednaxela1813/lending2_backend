import pytest
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from accounting.models import Company, ManagerProfile
from apps.dashboard.middleware import DashboardCompanyMiddleware


pytestmark = pytest.mark.django_db
User = get_user_model()

def test_request_company_is_set_for_manager():
    c = Company.objects.create(name="CompA", slug="compa")
    u = User.objects.create_user(email="a@a.sk", password="pass")
    ManagerProfile.objects.create(user=u, company=c, role="manager")
    req = RequestFactory().get("/dashboard/")
    req.user = u
    DashboardCompanyMiddleware().process_request(req)
    assert getattr(req, "company", None) == c

def test_request_company_is_none_for_anonymous():
    req = RequestFactory().get("/dashboard/")
    req.user = type("Anon", (), {"is_authenticated": False})()
    DashboardCompanyMiddleware().process_request(req)
    assert getattr(req, "company", None) is None
