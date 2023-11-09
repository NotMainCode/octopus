"""Serializers for the 'info' endpoints of 'Api' application v1."""

from rest_framework import serializers

from companies.models import Industry, Service, ServiceCategory


class IndustrySerializer(serializers.ModelSerializer):
    """Serializer for working with Industry resource."""

    class Meta:
        model = Industry
        fields = ("id", "name")


class ServiceBriefSerializer(serializers.ModelSerializer):
    """Brief serializer for working with Service resource."""

    class Meta:
        model = Service
        fields = ("id", "name")


class ServiceCategoryBriefSerializer(serializers.ModelSerializer):
    """Brief serializer for working with ServiceCategory resource."""

    class Meta:
        model = ServiceCategory
        fields = ("id", "name")


class ServiceCategorySerializer(ServiceCategoryBriefSerializer):
    """Serializer for working with ServiceCategory resource."""

    services = ServiceBriefSerializer(many=True)

    class Meta:
        model = ServiceCategory
        fields = (*ServiceCategoryBriefSerializer.Meta.fields, "services")
