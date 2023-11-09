"""URLs configuration of the 'info' endpoints of 'Api' app v1."""

from django.urls import path

from api.v1.info.views import industries, service_categories, services

urlpatterns = [
    path("industries/", industries, name="industries_list"),
    path("service_categories/", service_categories, name="service_categories_list"),
    path("services/", services, name="services_list"),
]
