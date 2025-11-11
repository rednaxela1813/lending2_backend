import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


@pytest.fixture
def user(db):
    """Обычный пользователь"""
    User = get_user_model()
    return User.objects.create_user(
        email="user@example.com",
        password="testpass123",
        full_name="Test User",
    )


@pytest.fixture
def superuser(db):
    """Суперпользователь"""
    User = get_user_model()
    return User.objects.create_superuser(
        email="admin@example.com",
        password="adminpass123",
    )


@pytest.fixture
def logged_in_client(client, user):
    """Клиент с залогиненным пользователем"""
    client.login(username=user.email, password="testpass123")
    return client



pytest_plugins = ["accounting.tests.conftest"]

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    # Даем доступ к БД всем тестам без явного @pytest.mark.django_db
    pass


# ⬇️ ДОПОЛНИМ: добавим properties-фикстуры к уже существующему подключению accounting
pytest_plugins = [
    "accounting.tests.conftest",
   # "apps.properties.tests.conftest",
]