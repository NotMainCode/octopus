"""Serializers describing responses of Auth endpoints for use in documentation."""
from rest_framework import serializers


class Response400Serializer(serializers.Serializer):
    """400 response: Invalid field value."""

    field_name = serializers.ListField(
        child=serializers.CharField(default="field_error")
    )


class Response403ActiveSerializer(serializers.Serializer):
    """403 response:  User status."""

    detail = serializers.CharField(default="User is active")


class Response403InactiveSerializer(serializers.Serializer):
    """403 response:  User status."""

    detail = serializers.CharField(default="User is inactive")
