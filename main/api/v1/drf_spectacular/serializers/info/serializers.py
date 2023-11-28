"""Serializers describing responses of Info endpoints for use in documentation."""

from rest_framework import serializers

from api.v1.info.filters import SEARCH_PARAM_REQUIRED_MESSAGE
from api.v1.info.serializers import (
    InfoCompanyBriefSerializer,
    InfoServiceBriefSerializer,
)


class SearchServicesCompaniesResponse200Serializer(serializers.Serializer):
    """Response 200: search_services_companies/ endpoint."""

    companies = InfoCompanyBriefSerializer(many=True)
    services = InfoServiceBriefSerializer(many=True)


class RequestParameterRequiredResponse400Serializer(serializers.Serializer):
    """400 response: request parameter required."""

    query_param = serializers.CharField(default=SEARCH_PARAM_REQUIRED_MESSAGE)
