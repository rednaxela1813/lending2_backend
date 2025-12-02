"""
Global fixtures for pytest.

This file lives at the project root (rootdir = /app).
Add plugins and fixtures here to make them available to all tests.
"""

import pytest

# Enable plugins globally here if needed.
# Example: pytest_plugins = ["dashboard.tests.fixtures"]

# pytest_plugins = []  # leave empty if no plugins are required


# Example of a global fixture: APIClient available in any test
from rest_framework.test import APIClient


@pytest.fixture
def client():
    """Convenience fixture for DRF APIClient."""
    return APIClient()


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Automatically provide DB access to all tests to avoid repeating @pytest.mark.django_db.
    """
    pass
