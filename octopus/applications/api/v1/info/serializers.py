"""Serializers for the 'info' endpoints of 'Api' application v1."""

from rest_framework import serializers

from applications.companies.models import (
    City,
    Company,
    Industry,
    Service,
    ServiceCategory,
)


class InfoIndustrySerializer(serializers.ModelSerializer):
    """Serializer for working with Industry resource."""

    class Meta:
        model = Industry
        fields = ("id", "name")


class InfoServiceBriefSerializer(serializers.ModelSerializer):
    """Brief serializer for working with Service resource."""

    class Meta:
        model = Service
        fields = ("id", "name")


class InfoServiceCategoryBriefSerializer(serializers.ModelSerializer):
    """Brief serializer for working with ServiceCategory resource."""

    class Meta:
        model = ServiceCategory
        fields = ("id", "name")


class InfoServiceCategorySerializer(InfoServiceCategoryBriefSerializer):
    """Serializer for working with ServiceCategory resource."""

    services = InfoServiceBriefSerializer(many=True)

    class Meta:
        model = ServiceCategory
        fields = (*InfoServiceCategoryBriefSerializer.Meta.fields, "services")


class InfoServiceSerializer(InfoServiceCategoryBriefSerializer):
    """Serializer for working with Service resource."""

    category = InfoServiceCategoryBriefSerializer()

    class Meta:
        model = Service
        fields = (*InfoServiceCategoryBriefSerializer.Meta.fields, "category")


class InfoCitySerializer(serializers.ModelSerializer):
    """Serializer for working with City resource."""

    class Meta:
        model = City
        fields = ("id", "name")


class InfoCompanyBriefSerializer(serializers.ModelSerializer):
    """Brief serializer for working with Company resource."""

    class Meta:
        model = Company
        fields = ("id", "name")
