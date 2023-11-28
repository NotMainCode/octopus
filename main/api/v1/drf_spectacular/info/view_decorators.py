"""Views decorators of Info endpoints for use in documentation."""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import status

from api.v1.drf_spectacular.info.serializers import (
    Response200SearchServicesCompaniesSerializer,
    Response400RequestParameterRequiredSerializer,
)

INFO_VIEW_DECORATORS = {
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
                    "Search by companies and service names (partial match). "
                    "At least three characters are required"
                ),
            ),
        ],
        responses={
            status.HTTP_200_OK: Response200SearchServicesCompaniesSerializer,
            status.HTTP_400_BAD_REQUEST: Response400RequestParameterRequiredSerializer,
        },
    ),
}
