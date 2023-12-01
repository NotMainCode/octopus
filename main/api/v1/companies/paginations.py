"""Pagination for the 'Api' application v1."""

from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        next_page = self.get_next_link()
        previous_page = self.get_previous_link()
        total_pages = self.page.paginator.num_pages
        return Response(
            {
                "total_pages": total_pages,
                "next_page": next_page,
                "previous_page": previous_page,
                "results": data,
            }
        )

    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "properties": {
                "total_pages": {
                    "type": "integer",
                    "example": 10,
                },
                "next_page": {
                    "type": "string",
                    "nullable": True,
                    "format": "uri",
                    "example": "http://api.example.org/accounts/?{page_query_param}=4".format(
                        page_query_param=self.page_query_param
                    ),
                },
                "previous_page": {
                    "type": "string",
                    "nullable": True,
                    "format": "uri",
                    "example": "http://api.example.org/accounts/?{page_query_param}=2".format(
                        page_query_param=self.page_query_param
                    ),
                },
                "results": schema,
            },
        }

    def get_page_size(self, request):
        if self.page_size_query_param is None:
            return self.page_size

        page_size = request.query_params.get(self.page_size_query_param)
        if page_size is None:
            return self.page_size

        return self.get_validated_page_size(page_size)

    def get_validated_page_size(self, page_size):
        try:
            if isinstance(page_size, float):
                raise ValueError
            validated_page_size = int(page_size)
        except (TypeError, ValueError):
            raise ValidationError({"page_size": "page_size value is not an integer."})

        if validated_page_size < 1:
            raise ValidationError({"page_size": "page_size value is less than 1."})

        return min(validated_page_size, self.max_page_size)
