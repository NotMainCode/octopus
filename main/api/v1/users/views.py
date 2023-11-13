"""Views for 'users' endpoints of 'Api' application v1."""
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode

from rest_framework import serializers, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.users.serializers import (
    ChangePasswordConfirmSerializer,
    GetUserSerializer,
    UpdateUserSerializer,
)

User = get_user_model()


class UserOwnPageView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user = User.objects.get(email=request.user.email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"user": "Пользователь не существует."})
        serializer = GetUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        try:
            user = User.objects.get(email=request.user.email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"user": "Пользователь не существует."})
        serializer = UpdateUserSerializer(
            user, data=request.data, context={"request": request}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def _generate_url(self, user, request):
        uid = force_str(urlsafe_base64_encode(force_bytes(user.id)))
        token = default_token_generator.make_token(user)
        site = get_current_site(request)
        protocol = "https:/" if request.is_secure() else "http:/"
        confirm_url = "/".join(
            (protocol, site.domain, "#", "change_password_confirm", uid, str(token))
        )
        return confirm_url

    def _generate_mail(self, url):
        mail = {}
        mail["subject"] = "password changes"
        mail["message"] = url
        return mail

    def post(self, request):
        try:
            user = User.objects.get(email=request.user.email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"user": "Пользователь не существует."})
        confirm_url = self._generate_url(user, request)
        mail = self._generate_mail(confirm_url)
        user.send_mail(user, mail)
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class UserChangePasswordConfirmView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ChangePasswordConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
