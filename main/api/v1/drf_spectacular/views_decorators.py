"""Views decorators for use in documentation."""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import status

from api.v1.drf_spectacular.serializers.info.serializers import (
    RequestParameterRequiredResponse400Serializer,
    SearchServicesCompaniesResponse200Serializer,
)

VIEWS_DECORATORS = {
    "InfoAPIView": extend_schema_view(
        get=extend_schema(
            tags=("info",),
        ),
    ),
    "search_services_companies": extend_schema(
        tags=("info",),
        description=(
            "Search on the main page - lists of companies and services "
            "(sorting by relevance of the search bar)"
        ),
        parameters=[
            OpenApiParameter(
                name="name",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=True,
                description=(
                    "Search by company and service names (partial match). "
                    "At least three characters are required"
                ),
            ),
        ],
        responses={
            status.HTTP_200_OK: SearchServicesCompaniesResponse200Serializer,
            status.HTTP_400_BAD_REQUEST: RequestParameterRequiredResponse400Serializer,
        },
    ),
}
