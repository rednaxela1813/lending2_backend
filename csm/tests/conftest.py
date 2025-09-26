"""
Глобальные фикстуры для pytest.

Этот файл находится в корне проекта (rootdir = /app).
Здесь можно подключить плагины и определить фикстуры,
которые будут доступны во всех тестах.
"""

import pytest

# ✅ Подключаем плагины на глобальном уровне
# если у тебя были плагины в dashboard/tests/conftest.py — перенеси сюда
# пример:
# pytest_plugins = ["dashboard.tests.fixtures"]

#pytest_plugins = []  # оставь пустым, если нет своих плагинов


# 🔹 Пример глобальной фикстуры: APIClient
# можно использовать client в любом тесте без импорта
from rest_framework.test import APIClient


@pytest.fixture
def client():
    """Упрощённый доступ к DRF APIClient"""
    return APIClient()


# 🔹 Пример фикстуры с настройками
@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Автоматически даём доступ к базе всем тестам.
    Убирает необходимость писать @pytest.mark.django_db каждый раз.
    """
    pass
