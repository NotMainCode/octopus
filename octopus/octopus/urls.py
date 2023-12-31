"""URL configuration of the 'octopus' application."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/", include("applications.api.urls")),
    path("admin/", admin.site.urls),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

if settings.DEBUG:
    urlpatterns += (
        path("__debug__/", include("debug_toolbar.urls")),
        path("api-auth/", include("rest_framework.urls")),
    )
