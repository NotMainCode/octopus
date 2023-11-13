"""Serializers for the 'users' endpoints of 'Api' application v1."""
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from users.validators import (
    CustomPasswordValidator,
    validate_first_name_and_last_name_fields,
)

User = get_user_model()
validator = CustomPasswordValidator()


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email")


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email")
        read_only_fields = ("email", "password")

    def validate(self, attrs):
        for value in attrs.values():
            validate_first_name_and_last_name_fields(value)
        return attrs


class ChangePasswordConfirmSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    uid = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    current_password = serializers.CharField(write_only=True, label="Текущий пароль")
    new_password = serializers.CharField(write_only=True, label="Новый пароль")
    re_new_password = serializers.CharField(
        write_only=True, label="Повтор нового пароля"
    )

    def validate(self, attrs):
        if attrs["new_password"] != attrs["re_new_password"]:
            raise serializers.ValidationError("Введены разные пароли.")
        if attrs["current_password"] == attrs["new_password"]:
            raise serializers.ValidationError("Текущий пароль и новый совпадают.")
        uid = attrs["uid"]
        encode_token = attrs["token"]
        try:
            id = int(force_str(urlsafe_base64_decode(uid)))
            self.user = User.objects.get(pk=id)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {"uid": "Неверный id или пользователь не существует."}
            )
        if not default_token_generator.check_token(self.user, encode_token):
            raise serializers.ValidationError(
                {"token": "Некорректный токен или срок его действия истёк."}
            )
        if not self.user.check_password(attrs["current_password"]):
            raise serializers.ValidationError(
                {"current_password": "Неверный текущий пароль."}
            )
        if not self.user.is_active:
            raise PermissionDenied("User is inactive.")
        return attrs

    def validate_new_password(self, value):
        validator.validate(value)
        return value
