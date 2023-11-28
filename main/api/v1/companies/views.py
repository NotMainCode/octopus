"""Views for 'companies' endpoints of 'Api' application v1."""

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.companies.filters import CompanyFilterSet
from api.v1.companies.paginations import CustomPagination
from api.v1.companies.serializers import CompanyDetailSerializer, CompanySerializer
from api.v1.drf_spectacular.custom_decorators import (
    activate_drf_spectacular_view_decorator,
)
from companies.models import Company, Favorite


class CompanyViewSet(viewsets.ModelViewSet):
    """URL requests handler to 'Company' resource endpoints."""

    queryset = Company.objects.all()
    pagination_class = CustomPagination
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CompanyFilterSet
    filterset_fields = ("city", "service", "is_favorited")

    def get_serializer_class(self):
        if self.action == "list":
            return CompanySerializer
        return CompanyDetailSerializer


@activate_drf_spectacular_view_decorator
class FavoriteAPIView(APIView):
    """URL requests handler to 'FavoritesList' resource endpoints."""

    def post(self, request, **kwargs):
        user = request.user
        company = get_object_or_404(Company, id=kwargs["id"])
        if Favorite.objects.filter(user=user, company=company).exists():
            raise exceptions.ValidationError(
                {"detail": "Компания добавлена в избранное ранее."}
            )

        Favorite.objects.create(user=user, company=company)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, **kwargs):
        user = request.user
        company = get_object_or_404(Company, id=kwargs["id"])
        favorite = Favorite.objects.filter(user=user, company=company).first()
        if not favorite:
            raise exceptions.ValidationError(
                {"detail": "Компании не было в избранном."}
            )

        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
