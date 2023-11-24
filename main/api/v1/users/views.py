"""Views for 'users' endpoints of 'Api' application v1."""
from django.contrib.auth import get_user_model

from rest_framework import status, views
from rest_framework.response import Response

from api.v1.drf_spectacular.custom_decorators import (
    activate_drf_spectacular_view_decorator,
)
from api.v1.users.serializers import ChangePasswordSerializer, UserSerializer

User = get_user_model()


@activate_drf_spectacular_view_decorator
class UserOwnPageView(views.APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserSerializer(
            request.user, data=request.data, context={"request": request}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@activate_drf_spectacular_view_decorator
class UserChangePasswordView(views.APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(
            request.user, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
