"""URLs configuration of the 'info' endpoints of 'Api' app v1."""

from django.urls import path

from api.v1.info.views import industries

urlpatterns = [
    path("industries/", industries, name="industries_list"),
]
