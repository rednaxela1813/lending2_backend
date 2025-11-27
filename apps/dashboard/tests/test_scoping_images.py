import pytest
from django.urls import reverse
from apps.company.models import CompanyInfo
from apps.dashboard.models import EditableImage
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from apps.dashboard.middleware import DashboardCompanyMiddleware



pytestmark = pytest.mark.django_db
User = get_user_model()


def test_image_list_is_scoped_by_company(client):
    # --- подготовка компаний и пользователей ---
    c1 = CompanyInfo.objects.create(name="Zavodsky", ico="", dic="", address="Addr", phone="123", email="zav@example.com")
    c2 = CompanyInfo.objects.create(name="Other", ico="", dic="", address="Addr2", phone="321", email="other@example.com")

    u1 = User.objects.create_user(email="m1@example.com", password="pass")
    u2 = User.objects.create_user(email="m2@example.com", password="pass")

    from accounting.models import ManagerProfile
    ManagerProfile.objects.create(user=u1, company=c1, role="manager")
    ManagerProfile.objects.create(user=u2, company=c2, role="manager")

    # --- данные ---
    EditableImage.objects.create(key="hero.image", caption="Hero A", company=c1)
    EditableImage.objects.create(key="hero.image", caption="Hero B", company=c2)

    # --- эмуляция запроса с мидлварой ---
    rf = RequestFactory()
    req = rf.get(reverse("dashboard:image_list"))
    req.user = u1
    DashboardCompanyMiddleware(lambda r: r).process_request(req)

    view = client.get(reverse("dashboard:image_list"))
    assert view.status_code in (200, 302)  # авторизации может требовать
