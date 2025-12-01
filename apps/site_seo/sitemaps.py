from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.properties.models import Property


class StaticViewSitemap(Sitemap):
    priority = 0.6
    changefreq = "weekly"

    def items(self):
        return [
            "csm:homepage",
            "property_list",
            "address_list",
            "billboard_list",
            "csm:hot_deals",
            "csm:privacy",
            "csm:terms",
            "csm:copyright",
            "csm:cookies",
            "csm:sitemap",
            "privacy_policy",
            "about_us",
        ]

    def location(self, item):
        return reverse(item)


class PropertySitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return Property.objects.order_by("-created_at")

    def lastmod(self, obj):
        return getattr(obj, "created_at", None)

    def location(self, obj):
        return obj.get_absolute_url()
