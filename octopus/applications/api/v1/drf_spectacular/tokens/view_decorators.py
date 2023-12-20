"""Views decorators of Tokens endpoints for use in documentation."""

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from applications.api.v1.drf_spectacular.serializers import (
    Response400Serializer,
    Response401Serializer,
)

TOKENS_VIEW_DECORATORS = {
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
}
