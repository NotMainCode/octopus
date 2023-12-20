"""URLs configuration of the 'companies' endpoints of 'Api' app v1."""

from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from applications.api.v1.companies.views import CompanyViewSet, FavoriteAPIView

router_v1 = DefaultRouter()
router_v1.register("", CompanyViewSet, basename="companies")

urlpatterns = [
    re_path(r"^(?P<id>\d+)/favorite/$", FavoriteAPIView.as_view(), name="favorite"),
    path("", include(router_v1.urls)),
]
