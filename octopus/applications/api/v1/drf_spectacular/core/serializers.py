"""Serializers describing responses for use in documentation."""

from rest_framework import serializers


class ResponseErrorSerializer(serializers.Serializer):
    """Response with errors."""

    detail = serializers.CharField(default="error text")


class Response400Serializer(serializers.Serializer):
    """400 response: Invalid field value."""

    field_name = serializers.ListField(
        child=serializers.CharField(default="field error")
    )


class Response401Serializer(ResponseErrorSerializer):
    """401 response: Invalid token value."""


class Response404Serializer(ResponseErrorSerializer):
    """404 response: Not found."""
