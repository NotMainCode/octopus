"""Helper functions for sending email to the user."""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from rest_framework.request import Request

User = get_user_model()

URL_PARTS_TO_CONFIRM = {
    "signup": "signup_confirm",
    "reset_password": "reset_password_confirm",
    "re_signup_confirm": "signup_confirm",
}

SUBJECTS_OF_EMAIL_TO_CONFIRM = {
    "signup": "Confirmation of registration",
    "reset_password": "Confirmation of password change",
    "re_signup_confirm": "Re-confirmation of registration",
}


def get_confirm_link(action: str, user: User, request: Request) -> str:
    """Create a link to confirm the action."""
    uid = force_str(urlsafe_base64_encode(force_bytes(user.id)))
    token = default_token_generator.make_token(user)
    site = get_current_site(request)
    protocol = "https:/" if request.is_secure() else "http:/"
    return "/".join((protocol, site.domain, "#", action, uid, str(token)))


def send_email_to_confirm(action: str, user: User, request: Request) -> None:
    """Send an email with a link to confirm the action."""
    confirm_link = get_confirm_link(action, user, request)
    user.email_user(
        subject=SUBJECTS_OF_EMAIL_TO_CONFIRM[action],
        message="Please follow the link to confirm the action {confirm_link}".format(
            confirm_link=confirm_link
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
    )
