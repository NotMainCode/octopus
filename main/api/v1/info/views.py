"""Views for 'info' endpoints of 'Api' application v1."""

from django.urls import resolve
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.v1.info.filters import InfoSearchFilter
from api.v1.info.serializers import (
    CitySerializer,
    CompanyBriefSerializer,
    IndustrySerializer,
    ServiceBriefSerializer,
    ServiceCategorySerializer,
    ServiceSerializer,
)
from companies.models import City, Company, Industry, Service, ServiceCategory

INFO_API_VIEW_SERIALIZERS = {
    "industries_list": IndustrySerializer,
    "service_categories_list": ServiceCategorySerializer,
    "services_list": ServiceSerializer,
    "cities_list": CitySerializer,
}

INFO_API_VIEW_MODELS = {
    "industries_list": Industry,
    "service_categories_list": ServiceCategory,
    "services_list": Service,
    "cities_list": City,
}


class InfoAPIView(ListAPIView):
    """URL requests handler for Info endpoints except search_services_companies."""

    authentication_classes = ()
    permission_classes = (AllowAny,)
    filter_backends = (InfoSearchFilter,)

    def get_queryset(self):
        return INFO_API_VIEW_MODELS[
            resolve(self.request.path_info).url_name
        ].objects.all()

    def get_serializer_class(self):
        return INFO_API_VIEW_SERIALIZERS[resolve(self.request.path_info).url_name]


@api_view()
@authentication_classes(())
@permission_classes((AllowAny,))
def search_services_companies(request):
    """URL requests handler for the search_services_companies/ endpoint."""
    companies = Company.objects.all()
    filter_companies = InfoSearchFilter().filter_queryset(
        request, companies, search_services_companies
    )
    companies_serializer = CompanyBriefSerializer(filter_companies, many=True)

    services = (
        Service.objects.filter(companies__isnull=False).distinct().values("id", "name")
    )
    filter_services = InfoSearchFilter().filter_queryset(
        request, services, search_services_companies
    )
    services_serializer = ServiceBriefSerializer(filter_services, many=True)

    return Response(
        data={
            "companies": companies_serializer.data,
            "services": services_serializer.data,
        },
        status=status.HTTP_200_OK,
    )
