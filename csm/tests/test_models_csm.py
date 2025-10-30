# csm/tests/test_models.py
import pytest
from csm.models import HeroSection, HeaderSection, FooterInfo, CompanyInfo

pytestmark = pytest.mark.django_db


def test_hero_section_str():
    obj = HeroSection.objects.create(title="T", subtitle="S")
    assert str(obj) == "Hero Section Content"


def test_header_section_str():
    obj = HeaderSection.objects.create(images="logo/test.png")
    assert str(obj) == "Header Content"


def test_footer_info_str():
    obj = FooterInfo.objects.create(
        about_description="About us",
        contact_email="e@e.com",
        contact_phone="123",
        contact_address="Addr",
    )
    assert str(obj) == "Footer Info"


def test_company_info_str():
    obj = CompanyInfo.objects.create(
        name="Comp", address="Addr", phone="1", email="e@e.com"
    )
    assert str(obj) == "Comp"
