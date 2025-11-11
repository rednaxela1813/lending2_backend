from apps.company.models import CompanyInfo




def test_company_info_str():
    obj = CompanyInfo.objects.create(
        name="Comp", address="Addr", phone="1", email="e@e.com"
    )
    assert str(obj) == "Comp"