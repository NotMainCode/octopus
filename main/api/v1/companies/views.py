"""Views for 'companies' endpoints of 'Api' application v1."""

from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from companies.models import City, Company

from .paginations import CustomPagination
from .serializers import CitySerializer, CompanyDetailSerializer, CompanySerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class = CitySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    pagination_class = CustomPagination
    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class = CompanySerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return CompanySerializer
        return CompanyDetailSerializer
