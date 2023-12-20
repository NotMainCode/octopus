"""URLs configuration of the 'Api' application v1."""

from django.urls import include, path

urlpatterns = [
    path("auth/", include("applications.api.v1.auth.urls")),
    path("companies/", include("applications.api.v1.companies.urls")),
    path("info/", include("applications.api.v1.info.urls")),
    path("tokens/", include("applications.api.v1.tokens.urls")),
    path("users/", include("applications.api.v1.users.urls")),
]
