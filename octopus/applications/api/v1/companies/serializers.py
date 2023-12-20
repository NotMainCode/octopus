"""Serializers for the 'companies' endpoints of 'Api' application v1."""

from rest_framework import serializers

from applications.companies.models import (
    City,
    Company,
    Industry,
    Service,
    ServiceCategory,
)


class CitySerializer(serializers.ModelSerializer):
    """Serializer for working with City resource."""

    class Meta:
        model = City
        fields = ("id", "name")


class ServiceCategoryBriefSerializer(serializers.ModelSerializer):
    """Brief serializer for working with ServiceCategory resource."""

    class Meta:
        model = ServiceCategory
        fields = ("id", "name")


class ServiceBriefSerializer(serializers.ModelSerializer):
    """Brief serializer for working with Service resource."""

    class Meta:
        model = Service
        fields = ("id", "name")


class IndustrySerializer(serializers.ModelSerializer):
    """Serializer for working with Industry resource."""

    class Meta:
        model = Industry
        fields = ("id", "name")


class ServiceSerializer(ServiceBriefSerializer):
    """Serializer for working with Service resource."""

    category = ServiceCategoryBriefSerializer()

    class Meta:
        model = Service
        fields = (*ServiceBriefSerializer.Meta.fields, "category")


class CompanyBriefSerializer(serializers.ModelSerializer):
    """Brief serializer for working with Company resource."""

    city = CitySerializer()
    services = ServiceBriefSerializer(many=True)
    industries = IndustrySerializer(many=True)
    is_favorited = serializers.BooleanField(read_only=True, default=False)

    class Meta:
        model = Company
        fields = (
            "id",
            "name",
            "logo",
            "city",
            "description",
            "services",
            "industries",
            "is_favorited",
        )


class CompanySerializer(serializers.ModelSerializer):
    """Serializer for working with Company resource."""

    city = CitySerializer()
    industries = IndustrySerializer(many=True)
    services = ServiceSerializer(many=True)
    is_favorited = serializers.BooleanField(read_only=True, default=False)
    phones = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = (
            "id",
            "name",
            "description",
            "email",
            "phones",
            "city",
            "address",
            "industries",
            "services",
            "logo",
            "website",
            "team_size",
            "year_founded",
            "is_favorited",
        )

    def get_phones(self, obj) -> list[str]:
        return obj.phones.values_list("number", flat=True)
