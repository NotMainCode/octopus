"""Views for the endpoints 'tokens' of 'Api' application v1."""

from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenRefreshView

from api.v1.drf_spectacular.custom_decorators import get_drf_spectacular_view_decorator


@get_drf_spectacular_view_decorator("tokens")
class CustomTokenRefreshView(TokenRefreshView):
    """Modified SimpleJWT TokenRefreshView.

    Added checking for user presence in the database and whether the user is active.
    """

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as exc:
            raise InvalidToken(exc.args[0])

        token = AccessToken(serializer.validated_data["access"])
        JWTAuthentication().get_user(token)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
