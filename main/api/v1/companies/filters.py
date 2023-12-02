from django.db.models import Count
from django_filters import rest_framework as filters

from companies.models import City, Company, Industry, Service


class CompanyFilterSet(filters.FilterSet):
    service = filters.ModelMultipleChoiceFilter(
        field_name="services", to_field_name="id", queryset=Service.objects.all()
    )
    city = filters.ModelMultipleChoiceFilter(
        field_name="city", to_field_name="id", queryset=City.objects.all()
    )
    industry = filters.ModelMultipleChoiceFilter(
        field_name="industries", to_field_name="id", queryset=Industry.objects.all()
    )
    is_favorited = filters.BooleanFilter(
        field_name="is_favorited", method="get_is_favorited_filter"
    )

    def get_is_favorited_filter(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(in_favorite__user=user)
        return queryset

    @property
    def qs(self):
        queryset = super().qs
        queryset = queryset.annotate(num_matches=Count("services"))
        queryset = queryset.annotate(num_matches=Count("industries"))
        queryset = queryset.order_by("-num_matches")
        return queryset

    class Meta:
        model = Company
        fields = ("city", "service", "industry", "is_favorited")
