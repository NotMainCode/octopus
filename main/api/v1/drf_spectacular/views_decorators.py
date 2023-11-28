"""Views decorators for use in documentation."""
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.v1.auth.serializers import (
    TokenUIDSerializer,
    UserResetPasswordConfirmSerializer,
    UserResetPasswordSerializer,
    UserSigninSerializer,
    UserSignupSerializer,
)
from api.v1.drf_spectacular.serializers.auth.serializers import (
    Response400Serializer,
    Response403ActiveSerializer,
    Response403InactiveSerializer,
)
from api.v1.drf_spectacular.serializers.info.serializers import (
    RequestParameterRequiredResponse400Serializer,
    SearchServicesCompaniesResponse200Serializer,
)

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
    "UserSignupView": extend_schema_view(
        post=extend_schema(
            tags=("auth",),
            request=UserSignupSerializer,
            responses={
                status.HTTP_200_OK: UserSignupSerializer,
                status.HTTP_400_BAD_REQUEST: Response400Serializer,
            },
        ),
    ),
    "UserSignupConfirmView": extend_schema_view(
        post=extend_schema(
            tags=("auth",),
            request=TokenUIDSerializer,
            responses={
                status.HTTP_204_NO_CONTENT: "",
                status.HTTP_400_BAD_REQUEST: Response400Serializer,
                status.HTTP_403_FORBIDDEN: Response403ActiveSerializer,
            },
        ),
    ),
    "UserSigninView": extend_schema_view(
        post=extend_schema(
            tags=("auth",),
            request=UserSigninSerializer,
            responses={
                status.HTTP_200_OK: TokenObtainPairSerializer,
                status.HTTP_400_BAD_REQUEST: Response400Serializer,
                status.HTTP_403_FORBIDDEN: Response403InactiveSerializer,
            },
        ),
    ),
    "UserResetPasswordView": extend_schema_view(
        post=extend_schema(
            tags=("auth",),
            request=UserResetPasswordSerializer,
            responses={
                status.HTTP_204_NO_CONTENT: "",
                status.HTTP_400_BAD_REQUEST: Response400Serializer,
                status.HTTP_403_FORBIDDEN: Response403InactiveSerializer,
            },
        ),
    ),
    "UserResetPasswordConfirmView": extend_schema_view(
        post=extend_schema(
            tags=("auth",),
            request=UserResetPasswordConfirmSerializer,
            responses={
                status.HTTP_204_NO_CONTENT: "",
                status.HTTP_400_BAD_REQUEST: Response400Serializer,
                status.HTTP_403_FORBIDDEN: Response403InactiveSerializer,
            },
        ),
    ),
}
