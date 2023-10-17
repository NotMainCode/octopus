"""URLs configuration of the 'api' application."""

from django.conf import settings
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

app_name = "api"

urlpatterns = [path("v1/", include("api.v1.urls"))]

if settings.DEBUG:
    urlpatterns += (
        path(
            "dynamic_doc/v1/download/",
            SpectacularAPIView.as_view(),
            name="schema",
        ),
        path(
            "redoc/v1/dynamic/",
            SpectacularRedocView.as_view(url_name="api:schema"),
            name="redoc_dynamic",
        ),
        path(
            "swagger/v1/dynamic/",
            SpectacularSwaggerView.as_view(url_name="api:schema"),
            name="swagger_dynamic",
        ),
    )
