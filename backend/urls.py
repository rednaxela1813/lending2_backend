from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('', include('csm.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', include('properties.urls')),
    # path('api/csm/', include([
    #     path('', include('csm.urls')),
    #     path('properties/', include('properties.urls')),
        
    #     # сюда же можно другие api-части
    # ])),
    # path('api/orders/', include('orders.urls')),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
