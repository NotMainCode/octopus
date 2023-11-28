"""Views decorators for use in documentation."""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from api.v1.companies.serializers import CompanyDetailSerializer, CompanySerializer
from api.v1.drf_spectacular.serializers.company.examples import (
    Response200CompaniesDetailExample,
)
from api.v1.drf_spectacular.serializers.info.serializers import (
    RequestParameterRequiredResponse400Serializer,
    SearchServicesCompaniesResponse200Serializer,
)
from api.v1.drf_spectacular.serializers.serializers import (
    Response400Serializer,
    Response401Serializer,
    Response404Serializer,
)
from api.v1.users.serializers import ChangePasswordSerializer, UserSerializer

VIEWS_DECORATORS = {
    "InfoAPIView": extend_schema_view(
        get=extend_schema(
            tags=("info",),
        ),
    ),
    "search_services_companies": extend_schema(
        tags=("info",),
        description=(
            "Search on the main page - lists of companies and services "
            "(sorting by relevance of the search bar)"
        ),
        parameters=[
            OpenApiParameter(
                name="name",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=True,
                description=(
                    "Search by company and service names (partial match). "
                    "At least three characters are required"
                ),
            ),
        ],
        responses={
            status.HTTP_200_OK: SearchServicesCompaniesResponse200Serializer,
            status.HTTP_400_BAD_REQUEST: RequestParameterRequiredResponse400Serializer,
        },
    ),
    "CustomTokenRefreshView": extend_schema_view(
        post=extend_schema(
            tags=("tokens",),
            responses={
                status.HTTP_200_OK: TokenRefreshSerializer,
                status.HTTP_400_BAD_REQUEST: Response400Serializer,
                status.HTTP_401_UNAUTHORIZED: Response401Serializer,
            },
        ),
    ),
    "UserOwnPageView": extend_schema_view(
        get=extend_schema(
            tags=("users",),
            responses={
                status.HTTP_200_OK: UserSerializer,
            },
        ),
        put=extend_schema(
            tags=("users",),
            request=UserSerializer,
            responses={
                status.HTTP_200_OK: UserSerializer,
                status.HTTP_400_BAD_REQUEST: Response400Serializer,
            },
        ),
    ),
    "UserChangePasswordView": extend_schema_view(
        post=extend_schema(
            tags=("users",),
            request=ChangePasswordSerializer,
            responses={
                status.HTTP_204_NO_CONTENT: OpenApiResponse(),
                status.HTTP_400_BAD_REQUEST: Response400Serializer,
            },
        ),
    ),
    "CompanyViewSet": extend_schema_view(
        list=extend_schema(
            tags=("companies",),
            responses={
                status.HTTP_200_OK: CompanySerializer,
                status.HTTP_400_BAD_REQUEST: Response400Serializer,
                status.HTTP_404_NOT_FOUND: Response404Serializer,
            },
        ),
        retrieve=extend_schema(
            tags=("companies",),
            responses={
                status.HTTP_200_OK: CompanyDetailSerializer,
                status.HTTP_400_BAD_REQUEST: Response400Serializer,
                status.HTTP_404_NOT_FOUND: Response404Serializer,
            },
            examples=[
                Response200CompaniesDetailExample,
            ],
        ),
    ),
    "FavoriteAPIView": extend_schema_view(
        post=extend_schema(
            tags=("favorite",),
            request=None,
            responses={
                status.HTTP_201_CREATED: OpenApiResponse(),
                status.HTTP_400_BAD_REQUEST: Response400Serializer,
                status.HTTP_401_UNAUTHORIZED: Response401Serializer,
                status.HTTP_404_NOT_FOUND: Response404Serializer,
            },
        ),
        delete=extend_schema(
            tags=("favorite",),
            responses={
                status.HTTP_204_NO_CONTENT: OpenApiResponse(),
                status.HTTP_400_BAD_REQUEST: Response400Serializer,
                status.HTTP_401_UNAUTHORIZED: Response401Serializer,
                status.HTTP_404_NOT_FOUND: Response404Serializer,
            },
        ),
    ),
}
