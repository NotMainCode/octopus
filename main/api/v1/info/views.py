"""Views for 'info' endpoints of 'Api' application v1."""

from django.urls import resolve
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from api.v1.info.serializers import (
    CitySerializer,
    IndustrySerializer,
    ServiceCategorySerializer,
    ServiceSerializer,
)
from companies.models import City, Industry, Service, ServiceCategory

INFO_SERIALIZERS = {
    "industries_list": IndustrySerializer,
    "service_categories_list": ServiceCategorySerializer,
    "services_list": ServiceSerializer,
    "cities_list": CitySerializer,
}

INFO_MODELS = {
    "industries_list": Industry,
    "service_categories_list": ServiceCategory,
    "services_list": Service,
    "cities_list": City,
}


class InfoAPIView(ListAPIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return INFO_MODELS[resolve(self.request.path_info).url_name].objects.all()

    def get_serializer_class(self):
        return INFO_SERIALIZERS[resolve(self.request.path_info).url_name]
