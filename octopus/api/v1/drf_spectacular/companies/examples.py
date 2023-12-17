"""Examples describing responses for use in documentation for companies/ endpoints."""

from drf_spectacular.utils import OpenApiExample
from rest_framework import status

Response200CompaniesDetailExample = OpenApiExample(
    name="CompaniesDetail",
    description="Example to response 200 for company detail.",
    response_only=True,
    status_codes=[str(status.HTTP_200_OK)],
    value={
        "id": 0,
        "name": "string",
        "description": "string",
        "email": "user@example.com",
        "phones": ["string"],
        "city": {"id": 0, "name": "string"},
        "address": "string",
        "industries": [{"id": 0, "name": "string"}],
        "services": [
            {"id": 0, "name": "string", "category": {"id": 0, "name": "string"}}
        ],
        "logo": "string",
        "website": "string",
        "team_size": 2147483647,
        "year_founded": 2100,
        "is_favorited": True,
    },
)
