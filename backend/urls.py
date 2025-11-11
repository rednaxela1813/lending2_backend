# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from accounting.views import ResolvingLoginView
from apps.company.views import about_us_view


urlpatterns = [
    
    path("pon_ka/", admin.site.urls),
    path('', include('csm.urls')),
    path('', include('apps.properties.urls')),
    path("kontakt/", include("contact_form.urls")),

 
    #path("__reload__/", include("django_browser_reload.urls")),
    # path('api/csm/', include([...]))
    
    # стандартные auth-URL (дадут password_reset и др.)
    path("accounts/", include("django.contrib.auth.urls")),
    
    # кастомный login/logout
    path("accounts/login/", ResolvingLoginView.as_view(), name="login"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    
    path("dashboard/", include("apps.dashboard.urls", namespace="dashboard")),
    path("api/", include("orders.urls")),
    path("", include("apps.contact_messages.urls")),
    path("about/", about_us_view, name="about_us"),
    path(
        "privacy-policy/",
        TemplateView.as_view(
            template_name="legal/privacy_policy.html",
            extra_context={
                "policy_version": getattr(settings, "PRIVACY_POLICY_VERSION", "v1"),
                "policy_updated": getattr(settings, "PRIVACY_POLICY_UPDATED", "2025-10-01"),
            },
        ),
        name="privacy_policy",
    ),
    #path("", include("apps.hotdeal.urls", namespace="hotdeal")),
    path("hot-deals/", include(("apps.hotdeal.urls", "hotdeal"), namespace="hotdeal")),
     
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
