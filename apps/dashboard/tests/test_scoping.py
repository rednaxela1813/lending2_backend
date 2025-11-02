import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounting.models import Company, ManagerProfile
from apps.dashboard.models import EditableText


pytestmark = pytest.mark.django_db
User = get_user_model()

@pytest.fixture
def c1():
    return Company.objects.create(name="Zavodsky", slug="zavodsky")

@pytest.fixture
def c2():
    return Company.objects.create(name="OtherCo", slug="other")

@pytest.fixture
def manager1(c1):
    u = User.objects.create_user(email="m1@example.com", password="pass")
    ManagerProfile.objects.create(user=u, company=c1)
    return u

@pytest.fixture
def manager2(c2):
    u = User.objects.create_user(email="m2@example.com", password="pass")
    ManagerProfile.objects.create(user=u, company=c2)
    return u

def test_text_list_is_scoped_by_company(client, manager1, manager2, c1, c2):
    EditableText.objects.create(key="hero.title", title="Hero C1", language="sk", text="...", company=c1)
    EditableText.objects.create(key="hero.title", title="Hero C2", language="sk", text="...", company=c2)
    EditableText.objects.create(key="public", title="Global", language="en", text="...")  # без company → глобально

    client.login(username=manager1.email, password="pass")
    resp1 = client.get(reverse("dashboard:text_list"))
    html1 = resp1.content.decode()
    assert "Hero C1" in html1 and "Global" in html1 and "Hero C2" not in html1
    client.logout()

    client.login(username=manager2.email, password="pass")
    resp2 = client.get(reverse("dashboard:text_list"))
    html2 = resp2.content.decode()
    assert "Hero C2" in html2 and "Global" in html2 and "Hero C1" not in html2
