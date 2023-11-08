"""Serializers for the 'info' endpoints of 'Api' application v1."""

from rest_framework import serializers

from companies.models import Industry


class IndustrySerializer(serializers.ModelSerializer):
    """Serializer for working with Industry resource."""

    class Meta:
        model = Industry
        fields = ("id", "name")
