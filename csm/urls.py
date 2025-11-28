from django.urls import path
#from .api_views import HeroSectionView, HeaderSectionView, FooterInfoView, CompanyInfoView,  ContactRequestView, ActiveThemeAPIView
from .views import ServicesListView, ServiceDetailView, ServiceOffersListView, footer_section
from .views import homepage, HotDealsPageView
from django.views.generic import TemplateView
from django.conf import settings

app_name = "csm"


urlpatterns = [
    # path('hero/', HeroSectionView.as_view(), name='hero-section'),
    # path('header/', HeaderSectionView.as_view(), name='header-section'),
    # path('footer/', FooterInfoView.as_view(), name='footer-info'),
    # path('company-info/', CompanyInfoView.as_view(), name='company-info'),
    # # path("send/", ContactFormView.as_view(), name="contact-send"),
    # path('contact/', ContactRequestView.as_view(), name='contact-form'),
    # path('theme/', ActiveThemeAPIView.as_view(), name='active-theme'),
    path('', homepage, name='homepage'),
    #path('services/<slug:service_type>/', ServicesListView.as_view(), name='services_list'),

    path("zasady-ochrany-osobnych-udajov/", TemplateView.as_view(template_name="legal/privacy.html"), name="privacy"),
    path("prevadzkovatel/", TemplateView.as_view(template_name="legal/operator.html"), name="operator"),
    path("autorske-prava/", TemplateView.as_view(template_name="legal/copyright.html"), name="copyright"),
    path("podmienky-pouzivania/", TemplateView.as_view(template_name="legal/terms.html"), name="terms"),
    path(
        "zasady-pouzivania-cookies/",
        TemplateView.as_view(
            template_name="legal/cookies.html",
            extra_context={
                "cookies_version": getattr(settings, "COOKIES_POLICY_VERSION", "v1"),
                "cookies_updated": getattr(settings, "COOKIES_POLICY_UPDATED", "2025-10-01"),
            },
        ),
        name="cookies",
    ),
    path(
        "mapa-stranok/",
        TemplateView.as_view(
            template_name="legal/sitemap.html",
            extra_context={
                "sitemap_updated": getattr(settings, "SITEMAP_UPDATED", "2025-10-01"),
            },
        ),
        name="sitemap",
    ),
    path("hot-deals/", HotDealsPageView.as_view(), name="hot_deals"),
    path("services/<uuid:pk>/", ServiceDetailView.as_view(), name="service_detail"),
    path("services/<slug:type>/offers/", ServiceOffersListView.as_view(), name="service_offers"),
   # path("footer/", footer_section, name="footer_section", name="footer_section"),
    
    #path('services/<slug:service_type>/', ServicesListView.as_view(), name='services'),
     
    
]
