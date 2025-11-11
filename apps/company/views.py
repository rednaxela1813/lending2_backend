from django.shortcuts import render

from .models import AboutUsPage


def about_us_view(request):
    """View to display the About Us page with company information and working hours."""
    about_us_page = (
        AboutUsPage.objects.select_related('company')
        .prefetch_related(
            "company__opening_hours",
            "company__special_openings",
        )
        .first()
    )

    company = about_us_page.company if about_us_page else None

    opening_hours = company.opening_hours.all() if company else []
    special_openings = company.special_openings.all() if company else []

    context = {
        "about_us_page": about_us_page,
        "company": company,
        "opening_hours": opening_hours,
        "special_openings": special_openings,
    }
    return render(request, "company/about_us.html", context)

