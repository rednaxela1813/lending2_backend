from apps.company.models import CompanyInfo, FooterInfo


def test_footer_info_str():
    company = CompanyInfo.objects.create(
        name="Comp",
        address="Addr",
        phone="123",
        email="e@e.com",
    )
    obj = FooterInfo.objects.create(
        company=company,
        about_description="About us",
        contact_email="e@e.com",
        contact_phone="123",
        contact_address="Addr",
    )
    assert str(obj) == "Footer: Comp"