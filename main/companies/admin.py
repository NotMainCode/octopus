from django.contrib import admin
from django.contrib.admin import TabularInline

from .models import Company, Industry, Phone, Service, ServiceCategory


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


class PhoneInline(TabularInline):
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


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ("company", "phone")
    list_filter = ("company__name",)
