"""Views for 'companies' endpoints of 'Api' application v1."""

from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from applications.api.v1.companies.filters import CompanyFilterSet
from applications.api.v1.companies.paginations import CustomPagination
from applications.api.v1.companies.serializers import (
    CompanyBriefSerializer,
    CompanySerializer,
)
from applications.api.v1.drf_spectacular.custom_decorators import (
    get_drf_spectacular_view_decorator,
)
from applications.companies.models import Company, Favorite


@get_drf_spectacular_view_decorator("companies")
class CompanyViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    """Handler for URL requests to the Company resource endpoints."""

    pagination_class = CustomPagination
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CompanyFilterSet
    filterset_fields = ("city", "service", "is_favorited")

    def get_serializer_class(self):
        if self.action == "list":
            return CompanyBriefSerializer
        return CompanySerializer

    def get_queryset(self):
        user_id = self.request.user.id or None
        subquery_favorite = Favorite.objects.filter(
            user_id=user_id, company=OuterRef("pk")
        )
        return (
            Company.objects.select_related("city")
            .prefetch_related("services", "industries")
            .annotate(
                is_favorited=(Exists(subquery_favorite)),
            )
        )


@get_drf_spectacular_view_decorator("companies")
class FavoriteAPIView(APIView):
    """Handler for URL requests to the Favorite resource endpoints."""

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
