"""Views for 'auth' endpoints of 'Api' application v1."""

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import resolve
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from rest_framework import status, views
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.v1.auth.serializers import (
    TokenUIDSerializer,
    UserResetPasswordConfirmSerializer,
    UserResetPasswordSerializer,
    UserReSignupConfirmSerializer,
    UserSigninSerializer,
    UserSignupSerializer,
)
from api.v1.drf_spectacular.custom_decorators import get_drf_spectacular_view_decorator

User = get_user_model()


class BaseView:
    permission_classes = (AllowAny,)

    action_list = {
        "signup": "registration",
        "signin": "login to your personal account",
        "reset_password": "password change",
        "re_signup_confirm": "resending registration confirmation",
    }

    def get_serializer_class(self, action):
        if action == "signup":
            return UserSignupSerializer
        if action == "signup_confirm":
            return TokenUIDSerializer
        if action == "signin":
            return UserSigninSerializer
        if action == "reset_password":
            return UserResetPasswordSerializer
        if action == "re_signup_confirm":
            return UserReSignupConfirmSerializer
        return UserResetPasswordConfirmSerializer

    def _generate_url(self, action, user, request):
        uid = force_str(urlsafe_base64_encode(force_bytes(user.id)))
        token = default_token_generator.make_token(user)
        site = get_current_site(request)
        protocol = "https:/" if request.is_secure() else "http:/"
        if action == "re_signup_confirm":
            confirm_url = "/".join(
                (protocol, site.domain, "#", action[3:], uid, str(token))
            )
        else:
            confirm_url = "/".join(
                (protocol, site.domain, "#", action + "_confirm", uid, str(token))
            )
        return confirm_url

    def _generate_mail(self, action, url):
        mail = {}
        mail["subject"] = self.action_list[action]
        mail["message"] = url
        return mail


@get_drf_spectacular_view_decorator("auth")
class UserSignupView(BaseView, views.APIView):
    def post(self, request):
        action = resolve(request.path_info).url_name
        serializer = self.get_serializer_class(action)(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        confirm_url = self._generate_url(action, user, request)
        mail = self._generate_mail(action, confirm_url)
        user.send_mail(user, mail)
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


@get_drf_spectacular_view_decorator("auth")
class UserSignupConfirmView(BaseView, views.APIView):
    def post(self, request):
        action = resolve(request.path_info).url_name
        serializer = self.get_serializer_class(action)(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        if user.is_active:
            raise PermissionDenied("User is active.")
        user.is_active = True
        user.save(update_fields=["is_active"])
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


@get_drf_spectacular_view_decorator("auth")
class UserSigninView(BaseView, views.APIView):
    def post(self, request):
        action = resolve(request.path_info).url_name
        serializer = self.get_serializer_class(action)(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        token = RefreshToken.for_user(user)
        return Response(
            {"access": str(token.access_token), "refresh": str(token)},
            status=status.HTTP_200_OK,
        )


@get_drf_spectacular_view_decorator("auth")
class UserResetPasswordView(BaseView, views.APIView):
    def post(self, request):
        action = resolve(request.path_info).url_name
        serializer = self.get_serializer_class(action)(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        confirm_url = self._generate_url(action, user, request)
        mail = self._generate_mail(action, confirm_url)
        user.send_mail(user, mail)
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


@get_drf_spectacular_view_decorator("auth")
class UserResetPasswordConfirmView(BaseView, views.APIView):
    def post(self, request):
        action = resolve(request.path_info).url_name
        serializer = self.get_serializer_class(action)(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        if not user.is_active:
            raise PermissionDenied("User is inactive.")
        user.password = serializer.validated_data["new_password"]
        user.save(update_fields=["password"])
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


@get_drf_spectacular_view_decorator("auth")
class UserReSignupConfirmView(BaseView, views.APIView):
    def post(self, request):
        action = resolve(request.path_info).url_name
        serializer = self.get_serializer_class(action)(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        confirm_url = self._generate_url(action, user, request)
        mail = self._generate_mail(action, confirm_url)
        user.send_mail(user, mail)
        return Response(status=status.HTTP_204_NO_CONTENT)
