"""Serializers describing responses of Users endpoints for use in documentation."""
from rest_framework import serializers


class Response400Serializer(serializers.Serializer):
    """400 response: Invalid field value."""

    detail = serializers.CharField(default="error text")
