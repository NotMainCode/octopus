"""Admin site settings of the Companies app."""

from django.contrib import admin

from companies.models import (
    City,
    Company,
    Favorite,
    Industry,
    Phone,
    Service,
    ServiceCategory,
)


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    """Settings of Industry table on the admin site."""

    list_display = ("name",)


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    """Settings of ServiceCategory table on the admin site."""

    list_display = ("name",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Settings of Service table on the admin site."""

    list_display = ("name", "category")
    list_filter = ("category",)


class PhoneInline(admin.TabularInline):
    """Settings for presenting Phone model in Company model."""

    model = Phone
    extra = 1


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Settings of Company table on the admin site."""

    list_display = ("name", "email", "year_founded")
    list_filter = ("industries", "services")
    search_fields = ("name", "description", "email")
    filter_horizontal = ("industries", "services")
    list_per_page = 20
    inlines = [PhoneInline]

    @admin.display(description="Избранное")
    def is_favorited(self, obj):
        return obj.favorite.count()


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """Settings of City table on the admin site."""

    list_display = ("pk", "name")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Settings of Favorite table on the admin site."""

    list_display = ("pk", "user", "company")
