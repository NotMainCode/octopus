"""Views for 'auth' endpoints of 'Api' application v1."""
from django.contrib.auth import get_user_model, tokens
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt import tokens

from ..auth.serializers import (
    TokenUIDSerializer,
    UserSerializer,
    UserSigninSerializer,
    UserSignupSerializer,
    UserResetPasswordConfirmSerializer,
    UserResetPasswordSerializer,
)
from ..auth.permissions import IsReadOnly


User = get_user_model()

action_list = {
    "signup": "registration",
    "signin": "login to your personal account",
    "reset_password": "password change",
}


class CustomAuthModel(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsReadOnly]

    def get_serializer_class(self):
        if self.action == "signup":
            return UserSignupSerializer
        elif self.action == "signup_confirm":
            return TokenUIDSerializer
        elif self.action == "signin":
            return UserSigninSerializer
        elif self.action == "signin_confirm":
            return TokenUIDSerializer
        elif self.action == "reset_password":
            return UserResetPasswordSerializer
        elif self.action == "reset_password_confirm":
            return UserResetPasswordConfirmSerializer
        else:
            return UserSerializer

    def _generate_URL(self, user, request):
        uid = force_str(urlsafe_base64_encode(force_bytes(user.id)))
        token = default_token_generator.make_token(user)
        site = get_current_site(request)
        protocol = "https:/" if request.is_secure() else "http:/"
        confirm_url = "/".join(
            (protocol, site.domain, "#", str(self.action) + "_confirm", uid, str(token))
        )
        return confirm_url

    def _generate_mail(self, action, url):
        mail = dict()
        mail["subject"] = action_list[action]
        mail["message"] = url
        return mail

    @action(
        methods=["POST"],
        permission_classes=(AllowAny,),
        detail=False,
        url_path="signup",
    )
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            confirm_url = self._generate_URL(user, request)
            mail = self._generate_mail(self.action, confirm_url)
            user.send_mail(user, mail)
            return Response(
                "На почту отправлено письмо со ссылкой подтверждения",
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["POST"],
        permission_classes=(AllowAny,),
        detail=False,
        url_path="signup_confirm",
    )
    def signup_confirm(self, request):
        serializer = self.get_serializer(data=request.query_params)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            user.is_active = True
            user.save(update_fields=["is_active"])
            return Response("Пользователь активирован", status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["POST"],
        permission_classes=(AllowAny,),
        detail=False,
        url_path="signin",
    )
    def signin(self, request):
        email = request.data.get("email")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(email=email)
            confirm_url = self._generate_URL(user, request)
            mail = self._generate_mail(self.action, confirm_url)
            user.send_mail(user, mail)
            return Response(
                "На почту отправлено письмо со ссылкой подтверждения",
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["POST"],
        permission_classes=(AllowAny,),
        detail=False,
        url_path="signin_confirm",
    )
    def signin_confirm(self, request):
        serializer = self.get_serializer(data=request.query_params)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            token = tokens.RefreshToken.for_user(user)
            return Response(
                {"access": str(token.access_token), "refresh": str(token)},
                status=status.HTTP_200_OK,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["POST"],
        permission_classes=(AllowAny,),
        detail=False,
        url_path="reset_password",
    )
    def reset_password(self, request):
        email = request.data.get("email")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(email=email)
            confirm_url = self._generate_URL(user, request)
            mail = self._generate_mail(self.action, confirm_url)
            user.send_mail(user, mail)
            return Response(
                "На почту отправлено письмо со ссылкой подтверждения",
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["POST"],
        permission_classes=(AllowAny,),
        detail=False,
        url_path="reset_password_confirm",
    )
    def reset_password_confirm(self, request):
        data = dict()
        data["uid"] = request.query_params.get("uid")
        data["token"] = request.query_params.get("token")
        data["new_password"] = request.data.get("new_password")
        data["re_new_password"] = request.data.get("re_new_password")
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            user.password = request.data.get("new_password")
            user.save(update_fields=["password"])
            return Response(
                "Пароль изменен",
                status=status.HTTP_200_OK,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)
