"""Views for 'companies' endpoints of 'Api' application v1."""

from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from api.v1.companies.paginations import CustomPagination
from api.v1.companies.serializers import CompanyDetailSerializer, CompanySerializer
from companies.models import Company


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    pagination_class = CustomPagination
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == "list":
            return CompanySerializer
        return CompanyDetailSerializer
