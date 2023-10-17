"""URL configuration of the 'main' application."""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += (
        path("admin/api-auth/", include("rest_framework.urls")),
    )
