"""URLs configuration of the 'auth' endpoints of 'Api' app v1."""

from django.urls import path

from applications.api.v1.auth.views import (
    re_signup_confirm,
    reset_password,
    reset_password_confirm,
    signin,
    signup,
    signup_confirm,
)

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("signup_confirm/", signup_confirm, name="signup_confirm"),
    path("signin/", signin, name="signin"),
    path("reset_password/", reset_password, name="reset_password"),
    path(
        "reset_password_confirm/", reset_password_confirm, name="reset_password_confirm"
    ),
    path("re_signup_confirm/", re_signup_confirm, name="re_signup_confirm"),
]
