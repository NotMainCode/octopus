"""View decorators of Users endpoints for use in documentation."""

from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import status

from applications.api.v1.drf_spectacular.serializers import (
    Response400Serializer,
    Response401Serializer,
)
from applications.api.v1.users.serializers import (
    ChangePasswordSerializer,
    UserSerializer,
)

USERS_VIEW_DECORATORS = {
    "UserOwnPageView": extend_schema_view(
        get=extend_schema(
            tags=("users",),
            responses={
                status.HTTP_200_OK: UserSerializer,
                status.HTTP_401_UNAUTHORIZED: Response401Serializer,
            },
        ),
        put=extend_schema(
            tags=("users",),
            request=UserSerializer,
            responses={
                status.HTTP_200_OK: UserSerializer,
                status.HTTP_400_BAD_REQUEST: Response400Serializer,
                status.HTTP_401_UNAUTHORIZED: Response401Serializer,
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
                status.HTTP_401_UNAUTHORIZED: Response401Serializer,
            },
        ),
    ),
}
