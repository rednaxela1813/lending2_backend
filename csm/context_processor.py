from apps.company.models import CompanyInfo
from .models import HeaderSection, ServiceSection

def company_info(request):
    try:
        company = CompanyInfo.objects.first()
    except CompanyInfo.DoesNotExist:
        company = None

    # Fetch header/navigation content from DB so all pages share the same translations/content
    header_section = HeaderSection.objects.first()
    nas_sluzby = list(ServiceSection.objects.all())

    return {
        "COMPANY_NAME": company.name if company else "Bum",
        "COMPANY_ICO": company.ico if company else "",
        "COMPANY_DIC": company.dic if company else "",
        "COMPANY_ADDRESS": company.address if company else "",
        "COMPANY_PHONE": company.phone if company else "",
        "COMPANY_EMAIL": company.email if company else "",
        "company_info": company,
        "header_section": header_section,
        "nas_sluzby": nas_sluzby,
    }
