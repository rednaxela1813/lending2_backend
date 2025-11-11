# csm/tests/test_models.py
import pytest
from csm.models import HeroSection, HeaderSection

pytestmark = pytest.mark.django_db


def test_hero_section_str():
    obj = HeroSection.objects.create(title="T", subtitle="S")
    assert str(obj) == "Hero Section Content"


def test_header_section_str():
    obj = HeaderSection.objects.create()
    assert str(obj) == "Header Content"






