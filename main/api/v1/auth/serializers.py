"""Serializers for the 'auth' endpoints of 'Api' application v1."""

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction, utils
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from users.validators import CustomEmailValidator

User = get_user_model()


class TokenUIDSerializer(serializers.Serializer):
    """Serializer for processing requests containing uid, token."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        try:
            pk = int(force_str(urlsafe_base64_decode(attrs["uid"])))
            self.user = User.objects.get(pk=pk)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {"uid": "Неверный id или пользователь не существует."}
            )

        if not default_token_generator.check_token(self.user, attrs["token"]):
            raise serializers.ValidationError(
                {"token": "Некорректный токен или срок его действия истёк."}
            )

        return attrs


class UserSignupSerializer(serializers.ModelSerializer):
    """Serializer for requests to the endpoint /signup/."""

    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "re_password",
        )
        extra_kwargs = {"email": {"validators": (CustomEmailValidator(),)}}

    def validate_email(self, value):
        normalized_email = User.objects.normalize_email(value)
        if User.objects.filter(email=normalized_email).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже существует."
            )
        return normalized_email

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("re_password"):
            raise serializers.ValidationError("Введены разные пароли.")
        return attrs

    def create(self, validated_data):
        try:
            return self.perform_create(validated_data)
        except utils.IntegrityError:
            self.fail("cannot_create_user")

    @transaction.atomic
    def perform_create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSignupConfirmSerializer(TokenUIDSerializer):
    """Serializer for requests to the endpoint /signup_confirm/."""

    def validate(self, attrs):
        super().validate(attrs)
        if self.user.is_active:
            raise PermissionDenied("User is active.")
        return attrs


class UserSigninSerializer(serializers.Serializer):
    """Serializer for requests to the endpoint /signin/."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        normalized_email = User.objects.normalize_email(attrs["email"])

        try:
            self.user = User.objects.get(email=normalized_email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "Неверный email или пользователь не существует."}
            )

        if not self.user.check_password(attrs["password"]):
            raise serializers.ValidationError({"password": "Неверный пароль."})
        if not self.user.is_active:
            raise PermissionDenied("User is inactive.")

        return attrs


class UserResetPasswordSerializer(serializers.Serializer):
    """Serializer for requests to the endpoint /reset_password/."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    email = serializers.CharField()

    def validate(self, attrs):
        normalized_email = User.objects.normalize_email(attrs["email"])

        try:
            self.user = User.objects.get(email=normalized_email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "Неверный email или пользователь не существует."}
            )

        if not self.user.is_active:
            raise PermissionDenied("User is inactive.")

        return attrs


class UserResetPasswordConfirmSerializer(TokenUIDSerializer):
    """Serializer for requests to the endpoint /reset_password_confirm/."""

    new_password = serializers.CharField(write_only=True)
    re_new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        super().validate(attrs)
        if attrs["new_password"] != attrs["re_new_password"]:
            raise serializers.ValidationError("Введены разные пароли.")
        if not self.user.is_active:
            raise PermissionDenied("User is inactive.")
        return attrs

    def validate_new_password(self, value):
        validate_password(value)
        return value


class UserReSignupConfirmSerializer(serializers.Serializer):
    """Serializer for requests to the endpoint /re_signup_confirm/."""

    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        normalized_email = User.objects.normalize_email(attrs["email"])

        try:
            self.user = User.objects.get(email=normalized_email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "Неверный email или пользователь не существует."}
            )

        if not self.user.check_password(attrs["password"]):
            raise serializers.ValidationError({"password": "Неверный пароль."})
        if self.user.is_active:
            raise PermissionDenied("User is active.")

        return attrs
