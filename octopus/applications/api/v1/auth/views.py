"""Views for 'auth' endpoints of 'Api' application v1."""

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from applications.api.v1.auth.email_utilities import send_email_to_confirm
from applications.api.v1.auth.serializers import (
    UserResetPasswordConfirmSerializer,
    UserResetPasswordSerializer,
    UserReSignupConfirmSerializer,
    UserSigninSerializer,
    UserSignupConfirmSerializer,
    UserSignupSerializer,
)
from applications.api.v1.drf_spectacular.custom_decorators import (
    get_drf_spectacular_view_decorator,
)

User = get_user_model()


@get_drf_spectacular_view_decorator("auth")
@api_view(("POST",))
@permission_classes((AllowAny,))
def signup(request):
    """Create user instance and email the user to confirm registration."""
    serializer = UserSignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    send_email_to_confirm("signup", serializer.instance, request)
    return Response(status=status.HTTP_204_NO_CONTENT)


@get_drf_spectacular_view_decorator("auth")
@api_view(("POST",))
@permission_classes((AllowAny,))
def signup_confirm(request):
    """Confirm user registration and activate user."""
    serializer = UserSignupConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.user.is_active = True
    serializer.user.save(update_fields=["is_active"])
    return Response(status=status.HTTP_204_NO_CONTENT)


@get_drf_spectacular_view_decorator("auth")
@api_view(("POST",))
@permission_classes((AllowAny,))
def signin(request):
    """Authenticate user and issue JWT-tokens."""
    serializer = UserSigninSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    refresh_token = RefreshToken.for_user(serializer.user)
    return Response(
        {"access": str(refresh_token.access_token), "refresh": str(refresh_token)},
        status=status.HTTP_200_OK,
    )


@get_drf_spectacular_view_decorator("auth")
@api_view(("POST",))
@permission_classes((AllowAny,))
def reset_password(request):
    """Email the user to confirm password reset."""
    serializer = UserResetPasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    send_email_to_confirm("reset_password", serializer.user, request)
    return Response(status=status.HTTP_204_NO_CONTENT)


@get_drf_spectacular_view_decorator("auth")
@api_view(("POST",))
@permission_classes((AllowAny,))
def reset_password_confirm(request):
    """Reset user password."""
    serializer = UserResetPasswordConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.user.set_password(serializer.validated_data["new_password"])
    serializer.user.save(update_fields=["password"])
    return Response(status=status.HTTP_204_NO_CONTENT)


@get_drf_spectacular_view_decorator("auth")
@api_view(("POST",))
@permission_classes((AllowAny,))
def re_signup_confirm(request):
    """Re-confirm user registration and activate user."""
    serializer = UserReSignupConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    send_email_to_confirm("re_signup_confirm", serializer.user, request)
    return Response(status=status.HTTP_204_NO_CONTENT)
