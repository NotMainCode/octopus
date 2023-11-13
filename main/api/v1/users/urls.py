"""URLs configuration of the 'users' endpoints of 'Api' app v1."""
from django.urls import path

from api.v1.users.views import (
    UserChangePasswordConfirmView,
    UserChangePasswordView,
    UserOwnPageView,
)

urlpatterns = [
    path("me/", UserOwnPageView.as_view(), name="me"),
    path("change_password/", UserChangePasswordView.as_view(), name="change_password"),
    path(
        "change_password_confirm/",
        UserChangePasswordConfirmView.as_view(),
        name="change_password_confirm",
    ),
]
