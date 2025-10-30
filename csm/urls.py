from django.urls import path
#from .api_views import HeroSectionView, HeaderSectionView, FooterInfoView, CompanyInfoView,  ContactRequestView, ActiveThemeAPIView
from .views import ServicesListView
from .views import homepage
from django.views.generic import TemplateView


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
     
    
]
