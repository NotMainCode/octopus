"""Serializers describing responses of Info endpoints for use in documentation."""

from rest_framework import serializers

from api.v1.info.filters import SEARCH_PARAM_REQUIRED_MESSAGE
from api.v1.info.serializers import CompanyBriefSerializer, ServiceBriefSerializer


class SearchServicesCompaniesResponse200Serializer(serializers.Serializer):
    """Response 200: search_services_companies/ endpoint."""

    companies = CompanyBriefSerializer(many=True)
    services = ServiceBriefSerializer(many=True)


class RequestParameterRequiredResponse403Serializer(serializers.Serializer):
    """403 response: request parameter required."""

    detail = serializers.CharField(default=SEARCH_PARAM_REQUIRED_MESSAGE)
