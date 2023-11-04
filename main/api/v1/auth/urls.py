"""URLs configuration of the 'auth' endpoints of 'Api' app v1."""
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from ..auth.views import CustomAuthModel


v1_router = DefaultRouter()
v1_router.register("", CustomAuthModel, basename="auth")

app_name = "auth"


urlpatterns = [
    path("", include(v1_router.urls), name="router_urls"),
]
