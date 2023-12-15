from django.db.models import Count
from django_filters import rest_framework as filters

from companies.models import City, Company, Service


class CompanyFilterSet(filters.FilterSet):
    service = filters.ModelMultipleChoiceFilter(
        field_name="services", to_field_name="id", queryset=Service.objects.all()
    )
    city = filters.ModelMultipleChoiceFilter(
        field_name="city", to_field_name="id", queryset=City.objects.all()
    )
    is_favorited = filters.BooleanFilter(
        field_name="is_favorited", method="get_is_favorited_filter"
    )

    class Meta:
        model = Company
        fields = ("city", "service", "is_favorited")

    def get_is_favorited_filter(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(in_favorite__user=user)
        return queryset

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        queryset = queryset.annotate(num_matches_services=Count("services")).order_by(
            "-num_matches_services"
        )
        return queryset
