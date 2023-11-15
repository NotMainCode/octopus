"""Admin site settings of the 'Users' app."""
from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import (
    AdminPasswordChangeForm,
    ReadOnlyPasswordHashField,
    UserChangeForm,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from users.validators import CustomPasswordValidator

User = get_user_model()
validator = CustomPasswordValidator()


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Подтверждение пароля", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError("Пароли не совпадают")
        validator.validate(password1)
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(
        label="Пароль",
        help_text="Чтобы изменить пароль, заполните заполните <a href={}>форму</a>.".format(
            "../password/"
        ),
    )


class AdminPasswordChangeForm(AdminPasswordChangeForm):
    password1 = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "autofocus": True}
        ),
        strip=False,
    )
    password2 = forms.CharField(
        label=_("Повторить пароль"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
    )

    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают")
        validator.validate(password1)
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
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
