from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
    
    path("pon_ka/", admin.site.urls),
    path('', include('csm.urls')),
    path('', include('properties.urls')),
    path("kontakt/", include("contact_form.urls")),

 
    #path("__reload__/", include("django_browser_reload.urls")),
    # path('api/csm/', include([...]))
    path("accounts/", include("django.contrib.auth.urls")),
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
    path("api/", include("orders.urls")),
    path("", include("apps.contact_messages.urls")),
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
     
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
