import pytest
from django.contrib.auth import get_user_model
from accounting.models import Company, ManagerProfile

pytestmark = pytest.mark.django_db
User = get_user_model()

def test_create_company_and_manager_profile():
    c = Company.objects.create(name="Zavodsky s.r.o.", slug="zavodsky")
    u = User.objects.create_user(email="mgr@example.com", password="pass123")
    p = ManagerProfile.objects.create(user=u, company=c, role="manager")

    assert p.user.email == "mgr@example.com"
    assert p.company == c
    assert p.role == "manager"
    assert p.is_active is True
    assert str(p) == "mgr@example.com (Zavodsky s.r.o.)"

def test_is_admin_property():
    c = Company.objects.create(name="A", slug="a")
    u = User.objects.create_user(email="admin@example.com", password="x")
    p = ManagerProfile.objects.create(user=u, company=c, role="admin")
    assert p.is_admin is True
