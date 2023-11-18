"""Serializers for the 'users' endpoints of 'Api' application v1."""
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from users.validators import CustomPasswordValidator

User = get_user_model()
validator = CustomPasswordValidator()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email")
        read_only_fields = ("email",)


class ChangePasswordSerializer(serializers.Serializer):
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
        if not self.instance.check_password(attrs["current_password"]):
            raise serializers.ValidationError(
                {"current_password": "Неверный текущий пароль."}
            )
        if not self.instance.is_active:
            raise PermissionDenied("User is inactive.")
        return attrs

    def validate_new_password(self, value):
        validator.validate(value)
        return value

    def save(self, **kwargs):
        self.instance.set_password(self.validated_data["new_password"])
        self.instance.save(update_fields=["password"])
        return self.instance
