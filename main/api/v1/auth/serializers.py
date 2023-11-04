"""Serializers for the 'auth' endpoints of 'Api' application v1."""
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from rest_framework import serializers

from users.validators import CustomPasswordValidator


User = get_user_model()
validator = CustomPasswordValidator()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
        )


class TokenUIDSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        super().validate(attrs)
        uid = self.initial_data.get("uid")
        encode_token = self.initial_data.get("token")
        id = int(force_str(urlsafe_base64_decode(uid)))
        user = User.objects.get(id=id)
        if user:
            decode_token = default_token_generator.check_token(user, encode_token)
            return user if decode_token else None


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
        ok_pass = self.initial_data["password"] == self.initial_data["re_password"]
        if not ok_pass:
            raise ValidationError("Введены разные пароли!")
        attrs.pop("re_password")
        return super().validate(attrs)

    def validate_password(self, value):
        return validator.validate(value)


class UserSigninSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True, label="Пароль")

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
        )

    def validate_password(self, value):
        return validator.validate(value)


class UserResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.CharField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
        )


class UserResetPasswordConfirmSerializer(TokenUIDSerializer):
    def validate(self, attrs):
        ok_pass = (
            self.initial_data["new_password"] == self.initial_data["re_new_password"]
        )
        if not ok_pass:
            raise ValidationError("Введены разные пароли!")
        return super().validate(attrs)

    def validate_new_password(self, value):
        return validator.validate(value)
