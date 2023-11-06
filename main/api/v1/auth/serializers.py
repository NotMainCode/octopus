"""Serializers for the 'auth' endpoints of 'Api' application v1."""
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from rest_framework import serializers

from users.validators import CustomPasswordValidator


User = get_user_model()
validator = CustomPasswordValidator()


class TokenUIDSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    uid = serializers.CharField(write_only=True)
    token = serializers.CharField()

    def validate(self, attrs):
        uid = attrs["uid"]
        encode_token = attrs["token"]
        try:
            id = int(force_str(urlsafe_base64_decode(uid)))
            self.user = User.objects.get(pk=id)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {"uid": "Неверный id или пользователь не существует."}
            )
        decode_token = default_token_generator.check_token(self.user, encode_token)
        return attrs if decode_token else None


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, label="Пароль")
    re_password = serializers.CharField(write_only=True, label="Повтор пароля")

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

    def validate(self, attrs):
        attrs.pop("re_password")
        return attrs

    def validate_password(self, value):
        if value != self.initial_data["re_password"]:
            raise serializers.ValidationError("Введены разные пароли!")
        return validator.validate(value)


class UserSigninSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True, label="Пароль")

    def validate_password(self, value):
        return validator.validate(value)


class UserResetPasswordSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    email = serializers.CharField()

    def validate(self, attrs):
        try:
            self.user = User.objects.get(email=attrs["email"])
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {"email": "Неверный email или пользователь не существует."}
            )
        return attrs


class UserResetPasswordConfirmSerializer(TokenUIDSerializer):
    new_password = serializers.CharField(write_only=True, label="Пароль")
    re_new_password = serializers.CharField(write_only=True, label="Повтор пароля")

    def validate_password(self, value):
        if value != self.initial_data["re_password"]:
            raise serializers.ValidationError("Введены разные пароли!")
        return validator.validate(value)
