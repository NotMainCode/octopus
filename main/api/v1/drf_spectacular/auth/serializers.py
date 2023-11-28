"""Serializers describing responses of Auth endpoints for use in documentation."""

from rest_framework import serializers


class Response403UserIsActiveSerializer(serializers.Serializer):
    """403 response:  User status."""

    detail = serializers.CharField(default="User is active")


class Response403UserIsInactiveSerializer(serializers.Serializer):
    """403 response:  User status."""

    detail = serializers.CharField(default="User is inactive")
