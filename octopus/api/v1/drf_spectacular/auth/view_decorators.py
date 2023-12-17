"""Views decorators of Auth endpoints for use in documentation."""

from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.v1.auth.serializers import (
    UserResetPasswordConfirmSerializer,
    UserResetPasswordSerializer,
    UserReSignupConfirmSerializer,
    UserSigninSerializer,
    UserSignupConfirmSerializer,
    UserSignupSerializer,
)
from api.v1.drf_spectacular.auth.serializers import (
    Response403UserIsActiveSerializer,
    Response403UserIsInactiveSerializer,
)
from api.v1.drf_spectacular.serializers import Response400Serializer

AUTH_VIEW_DECORATORS = {
    "signup": extend_schema(
        tags=("auth",),
        request=UserSignupSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(),
            status.HTTP_400_BAD_REQUEST: Response400Serializer,
        },
    ),
    "signup_confirm": extend_schema(
        tags=("auth",),
        request=UserSignupConfirmSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: "",
            status.HTTP_400_BAD_REQUEST: Response400Serializer,
            status.HTTP_403_FORBIDDEN: Response403UserIsActiveSerializer,
        },
    ),
    "signin": extend_schema(
        tags=("auth",),
        request=UserSigninSerializer,
        responses={
            status.HTTP_200_OK: TokenObtainPairSerializer,
            status.HTTP_400_BAD_REQUEST: Response400Serializer,
            status.HTTP_403_FORBIDDEN: Response403UserIsInactiveSerializer,
        },
    ),
    "reset_password": extend_schema(
        tags=("auth",),
        request=UserResetPasswordSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: "",
            status.HTTP_400_BAD_REQUEST: Response400Serializer,
            status.HTTP_403_FORBIDDEN: Response403UserIsInactiveSerializer,
        },
    ),
    "reset_password_confirm": extend_schema(
        tags=("auth",),
        request=UserResetPasswordConfirmSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: "",
            status.HTTP_400_BAD_REQUEST: Response400Serializer,
            status.HTTP_403_FORBIDDEN: Response403UserIsInactiveSerializer,
        },
    ),
    "re_signup_confirm": extend_schema(
        tags=("auth",),
        request=UserReSignupConfirmSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(),
            status.HTTP_400_BAD_REQUEST: Response400Serializer,
            status.HTTP_403_FORBIDDEN: Response403UserIsActiveSerializer,
        },
    ),
}
