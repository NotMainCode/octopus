"""Admin site settings of the 'Users' app."""
from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ( "email", "first_name", "last_name")
    empty_value_display = '-пусто-'
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
