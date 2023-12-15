"""Views for 'users' endpoints of 'Api' application v1."""

from django.contrib.auth import get_user_model
from rest_framework import status, views
from rest_framework.response import Response

from api.v1.drf_spectacular.custom_decorators import get_drf_spectacular_view_decorator
from api.v1.users.serializers import ChangePasswordSerializer, UserSerializer

User = get_user_model()


@get_drf_spectacular_view_decorator("users")
class UserOwnPageView(views.APIView):
    """Handler of URL requests to the endpoint /me/."""

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserSerializer(
            request.user, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@get_drf_spectacular_view_decorator("users")
class UserChangePasswordView(views.APIView):
    """Handler of URL requests to the endpoint /change_password/."""

    def post(self, request):
        serializer = ChangePasswordSerializer(
            request.user, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
