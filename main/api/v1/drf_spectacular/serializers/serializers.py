"""Serializers describing responses for use in documentation."""
from rest_framework import serializers


class Response401Serializer(serializers.Serializer):
    """401 response: Invalid token value."""

    detail = serializers.CharField(default="error text")
