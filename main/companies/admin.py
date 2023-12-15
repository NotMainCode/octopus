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
    list_display = ("name",)


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)


class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 1


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
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
    list_display = ("pk", "name")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "company")
