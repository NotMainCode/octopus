"""Serializers describing responses of Users endpoints for use in documentation."""
from rest_framework import serializers

from api.v1.users.serializers import UserSerializer, ChangePasswordSerializer


class UserRequestSerializer(UserSerializer):
    """Request: users/me endpoint."""


class UserResponse200Serializer(UserSerializer):
    """Response 200: users/me endpoint."""


class PutUserResponse400Serializer(serializers.Serializer):
    """Response 400: users/me endpoint."""

    detail = serializers.CharField(default="error text")


class ChangePasswordRequestSerializer(ChangePasswordSerializer):
    """Request: users/change_password endpoint."""


class ChangePasswordResponse400Serializer(ChangePasswordSerializer):
    """Response 400: users/change_password endpoint."""

    detail = serializers.CharField(default="error text")
