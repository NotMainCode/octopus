"""Serializers describing responses of Companies endpoints for use in documentation."""

from rest_framework import serializers


class Response400QueryParamSerializer(serializers.Serializer):
    """400 response: Invalid field value."""

    query_param_name = serializers.ListField(
        child=serializers.CharField(default="query param error")
    )
