"""URLs configuration of the 'companies' endpoints of 'Api' app v1."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.companies.views import CompanyViewSet

router_v1 = DefaultRouter()
router_v1.register("", CompanyViewSet, basename="companies")

urlpatterns = [path("", include(router_v1.urls))]
