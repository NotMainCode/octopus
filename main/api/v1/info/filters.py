"""Filters for endpoints of the Info group."""

from django.db.models import Case, IntegerField, Value, When
from rest_framework import filters


class InfoSearchFilter(filters.SearchFilter):
    """Filter for endpoints of the Info group."""

    search_param = "name"

    def filter_queryset(self, request, queryset, view):
        name = request.query_params.get(self.search_param)
        if name is None:
            return queryset
        return (
            queryset.annotate(
                relevance_to_search=Case(
                    When(name__istartswith=name, then=Value(1)),
                    When(name__icontains=name, then=Value(2)),
                    default=0,
                    output_field=IntegerField(),
                )
            )
            .exclude(relevance_to_search=0)
            .order_by("relevance_to_search", "name")
        )
