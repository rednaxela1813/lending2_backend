from django.urls import path
from .api_views import HeroSectionView, HeaderSectionView, FooterInfoView, CompanyInfoView,  ContactRequestView


urlpatterns = [
    path('hero/', HeroSectionView.as_view(), name='hero-section'),
    path('header/', HeaderSectionView.as_view(), name='header-section'),
    path('footer/', FooterInfoView.as_view(), name='footer-info'),
    path('company-info/', CompanyInfoView.as_view(), name='company-info'),
    # path("send/", ContactFormView.as_view(), name="contact-send"),
    path('contact/', ContactRequestView.as_view(), name='contact-form'),
]
