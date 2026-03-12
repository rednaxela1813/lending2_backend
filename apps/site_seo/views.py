from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.sitemaps.views import sitemap as django_sitemap


def robots_txt(request):
    if not getattr(settings, "SITE_SEO_ENABLED", False):
        return HttpResponseNotFound()
    site_url = getattr(settings, "SITE_URL", "").rstrip("/")
    lines = [
        "User-agent: *",
        "Disallow: /pon_ka/",
        "Disallow: /accounts/",
        "Disallow: /contact/submit/",
        f"Sitemap: {site_url}/sitemap.xml" if site_url else "",
        "",
    ]
    content = "\n".join([line for line in lines if line is not None])
    return HttpResponse(content, content_type="text/plain")


def sitemap_view(request, sitemaps, **kwargs):
    if not getattr(settings, "SITE_SEO_ENABLED", False):
        return HttpResponseNotFound()
    return django_sitemap(request, sitemaps, **kwargs)
