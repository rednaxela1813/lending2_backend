from apps.company.models import CompanyInfo

def company_info(request):
    try:
        company = CompanyInfo.objects.first()
    except CompanyInfo.DoesNotExist:
        company = None

    return {
        "COMPANY_NAME": company.name if company else "Bum",
        "COMPANY_ICO": company.ico if company else "",
        "COMPANY_DIC": company.dic if company else "",
        "COMPANY_ADDRESS": company.address if company else "",
        "COMPANY_PHONE": company.phone if company else "",
        "COMPANY_EMAIL": company.email if company else "",
    }
