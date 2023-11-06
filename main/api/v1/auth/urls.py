"""URLs configuration of the 'auth' endpoints of 'Api' app v1."""
from django.urls import path

from api.v1.auth.views import (
    UserSignupView,
    UserSignupConfirmView,
    UserSigninView,
    UserSigninConfirmView,
    UserResetPasswordView,
    UserResetPasswordConfirmView,
)


urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="signup"),
    path("signup_confirm/", UserSignupConfirmView.as_view(), name="signup_confirm"),
    path("signin/", UserSigninView.as_view(), name="signin"),
    path("signin_confirm/", UserSigninConfirmView.as_view(), name="signin_confirm"),
    path("reset_password/", UserResetPasswordView.as_view(), name="reset_password"),
    path(
        "reset_password_confirm/",
        UserResetPasswordConfirmView.as_view(),
        name="reset_password_confirm",
    ),
]
