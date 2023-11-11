"""URLs configuration of the 'auth' endpoints of 'Api' app v1."""
from django.urls import path

from api.v1.auth.views import (
    UserResetPasswordConfirmView,
    UserResetPasswordView,
    UserSigninView,
    UserSignupConfirmView,
    UserSignupView,
)

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="signup"),
    path("signup_confirm/", UserSignupConfirmView.as_view(), name="signup_confirm"),
    path("signin/", UserSigninView.as_view(), name="signin"),
    path("reset_password/", UserResetPasswordView.as_view(), name="reset_password"),
    path(
        "reset_password_confirm/",
        UserResetPasswordConfirmView.as_view(),
        name="reset_password_confirm",
    ),
]
