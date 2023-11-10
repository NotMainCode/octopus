from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        next_page = self.get_next_link()
        previous_page = self.get_previous_link()
        total_pages = self.page.paginator.num_pages
        return Response({
            'total_pages': total_pages,
            'next_page': next_page,
            'previous_page': previous_page,
            'results': data
        })
