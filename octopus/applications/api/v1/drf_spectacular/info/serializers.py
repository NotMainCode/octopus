"""Serializers describing responses of Info endpoints for use in documentation."""

from rest_framework import serializers

from applications.api.v1.info.filters import SEARCH_PARAM_REQUIRED_MESSAGE
from applications.api.v1.info.serializers import (
    InfoCompanyBriefSerializer,
    InfoServiceBriefSerializer,
)


class Response200SearchServicesCompaniesSerializer(serializers.Serializer):
    """Response 200: search_services_companies/ endpoint."""

    companies = InfoCompanyBriefSerializer(many=True)
    services = InfoServiceBriefSerializer(many=True)


class Response400RequestParameterRequiredSerializer(serializers.Serializer):
    """400 response: request parameter required."""

    query_param = serializers.CharField(default=SEARCH_PARAM_REQUIRED_MESSAGE)
