from django.urls import path

from .sitemaps import PropertySitemap, StaticViewSitemap
from .views import robots_txt, sitemap_view


sitemaps = {
    "static": StaticViewSitemap,
    "properties": PropertySitemap,
}


urlpatterns = [
    path("sitemap.xml", sitemap_view, {"sitemaps": sitemaps}, name="sitemap_xml"),
    path("robots.txt", robots_txt, name="robots_txt"),
]
