"""Admin site settings of the Users app."""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Settings of User table on the admin site."""

    list_display = ("email", "first_name", "last_name")
    list_filter = ()
    empty_value_display = "-пусто-"
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    fieldsets = (
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "email", "password")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "email", "password1", "password2")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
