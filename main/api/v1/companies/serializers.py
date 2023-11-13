"""Serializers for the 'companies' endpoints of 'Api' application v1."""
from rest_framework import serializers

from companies.models import City, Company, Industry, Service, ServiceCategory


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name")


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ("id", "name")


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("id", "name")


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ("id", "name")


class CustomServiceSerializer(ServiceSerializer):
    category = ServiceCategorySerializer()

    class Meta:
        model = Service
        fields = ("id", "name", "category")


class CompanySerializer(serializers.ModelSerializer):
    """Сериализатор получения компании."""

    city = CitySerializer()
    services = ServiceSerializer(many=True)

    class Meta:
        model = Company
        fields = ("id", "name", "logo", "city", "description", "services")


class CompanyDetailSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    industries = IndustrySerializer(many=True)
    services = CustomServiceSerializer(many=True)

    class Meta:
        model = Company
        fields = (
            "id",
            "name",
            "description",
            "email",
            "city",
            "address",
            "industries",
            "services",
            "logo",
            "website",
            "team_size",
            "year_founded",
        )
