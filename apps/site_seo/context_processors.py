from django.conf import settings


def seo_settings(request):
    return {
        "SITE_URL": getattr(settings, "SITE_URL", "").rstrip("/"),
        "SITE_OG_IMAGE": getattr(settings, "SITE_OG_IMAGE", ""),
    }

