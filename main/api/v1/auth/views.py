"""Views for 'auth' endpoints of 'Api' application v1."""
from django.contrib.auth import get_user_model, tokens
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import resolve
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode

from rest_framework import status, views
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt import tokens

from api.v1.auth.serializers import (
    TokenUIDSerializer,
    UserSigninSerializer,
    UserSignupSerializer,
    UserResetPasswordConfirmSerializer,
    UserResetPasswordSerializer,
)


User = get_user_model()


class BaseView:
    permission_classes = (AllowAny,)

    action_list = {
        "signup": "registration",
        "signin": "login to your personal account",
        "reset_password": "password change",
    }

    def _generate_URL(self, action, user, request):
        uid = force_str(urlsafe_base64_encode(force_bytes(user.id)))
        token = default_token_generator.make_token(user)
        site = get_current_site(request)
        protocol = "https:/" if request.is_secure() else "http:/"
        confirm_url = "/".join(
            (protocol, site.domain, "#", action + "_confirm", uid, str(token))
        )
        return confirm_url

    def _generate_mail(self, action, url):
        mail = dict()
        mail["subject"] = self.action_list[action]
        mail["message"] = url
        return mail

    def get_serializer(self, action):
        if action == "signup":
            return UserSignupSerializer
        elif action == "signup_confirm":
            return TokenUIDSerializer
        elif action == "signin":
            return UserSigninSerializer
        elif action == "signin_confirm":
            return TokenUIDSerializer
        elif action == "reset_password":
            return UserResetPasswordSerializer
        return UserResetPasswordConfirmSerializer


class UserSignupView(BaseView, views.APIView):
    def post(self, request):
        action = resolve(request.path_info).url_name
        serializer = self.get_serializer(action)(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            confirm_url = self._generate_URL(action, user, request)
            mail = self._generate_mail(action, confirm_url)
            user.send_mail(user, mail)
            return Response(
                "На почту отправлено письмо со ссылкой подтверждения",
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserSignupConfirmView(BaseView, views.APIView):
    def post(self, request):
        serializer = self.get_serializer(action)(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            user.is_active = True
            user.save(update_fields=["is_active"])
            token = tokens.RefreshToken.for_user(user)
            return Response(
                {"access": str(token.access_token), "refresh": str(token)},
                status=status.HTTP_200_OK,
            )
        return (
            Response(status=status.HTTP_400_BAD_REQUEST)
            if user.is_active
            else Response(
                {"detail": "User is active"}, status=status.HTTP_403_FORBIDDEN
            )
        )


class UserSigninView(BaseView, views.APIView):
    def post(self, request):
        email = request.data.get("email")
        action = resolve(request.path_info).url_name
        serializer = self.get_serializer(action)(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=email)
            confirm_url = self._generate_URL(action, user, request)
            mail = self._generate_mail(action, confirm_url)
            user.send_mail(user, mail)
            return Response(
                "На почту отправлено письмо со ссылкой подтверждения",
                status=status.HTTP_204_NO_CONTENT,
            )
        return (
            Response(status=status.HTTP_400_BAD_REQUEST)
            if user.is_active
            else Response(
                {"detail": "User is inactive"}, status=status.HTTP_403_FORBIDDEN
            )
        )


class UserSigninConfirmView(BaseView, views.APIView):
    def post(self, request):
        serializer = self.get_serializer(action)(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            token = tokens.RefreshToken.for_user(user)
            return Response(
                {"access": str(token.access_token), "refresh": str(token)},
                status=status.HTTP_200_OK,
            )
        return (
            Response(status=status.HTTP_400_BAD_REQUEST)
            if user.is_active
            else Response(
                {"detail": "User is active"}, status=status.HTTP_403_FORBIDDEN
            )
        )


class UserResetPasswordView(BaseView, views.APIView):
    def post(self, request):
        action = resolve(request.path_info).url_name
        serializer = self.get_serializer(action)(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.user
            confirm_url = self._generate_URL(action, user, request)
            mail = self._generate_mail(action, confirm_url)
            user.send_mail(user, mail)
            return Response(
                "На почту отправлено письмо со ссылкой подтверждения",
                status=status.HTTP_204_NO_CONTENT,
            )
        return (
            Response(status=status.HTTP_400_BAD_REQUEST)
            if user.is_active
            else Response(
                {"detail": "User is inactive"}, status=status.HTTP_403_FORBIDDEN
            )
        )


class UserResetPasswordConfirmView(BaseView, views.APIView):
    def post(self, request):
        action = resolve(request.path_info).url_name
        data = dict()
        data["uid"] = request.data.get("uid")
        data["token"] = request.data.get("token")
        data["new_password"] = request.data.get("new_password")
        data["re_new_password"] = request.data.get("re_new_password")
        serializer = self.get_serializer(action)(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.user
            user.password = serializer.validated_data["new_password"]
            user.save(update_fields=["password"])
            return Response(
                "Пароль изменен",
                status=status.HTTP_204_NO_CONTENT,
            )
        return (
            Response(status=status.HTTP_400_BAD_REQUEST)
            if user.is_active
            else Response(
                {"detail": "User is inactive"}, status=status.HTTP_403_FORBIDDEN
            )
        )
