"""Validators for User model fields."""

import re

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, validate_ipv46_address
from django.utils.deconstruct import deconstructible
from django.utils.regex_helper import _lazy_re_compile
from django.utils.translation import gettext as _

from core.users.constants.field_limits import FIELD_LIMITS_USERS_APP


class CustomPasswordValidator:
    """User password validation."""

    MIN_LENGTH = FIELD_LIMITS_USERS_APP["password_min_char"]
    MAX_LENGTH = FIELD_LIMITS_USERS_APP["password_max_char"]

    def validate(self, password, user=None):
        """Validate user password."""
        if len(password) < self.MIN_LENGTH:
            raise ValidationError(
                "Минимальная длина пароля {min_length} символов!".format(
                    min_length=self.MIN_LENGTH
                )
            )
        if len(password) > self.MAX_LENGTH:
            raise ValidationError(
                "Максимальная длина пароля {max_length} символов!".format(
                    max_length=self.MAX_LENGTH
                )
            )
        if password.isdigit():
            raise ValidationError("Пароль не должен содержать только цифры!")

        unacceptable_simbols = "".join(
            set(re.sub(r"[a-zA-Zа-яА-ЯёЁ+-_.!?@%#№$^&*\d+=/]", "", password))
        )
        if unacceptable_simbols:
            raise ValidationError(
                "Символы <{unacceptable_simbols}> запрещены!".format(
                    unacceptable_simbols=unacceptable_simbols
                )
            )

    def get_help_text(self):
        """Get help text for the password field."""
        return (
            f"Ваш пароль должен содержать не менее {self.MIN_LENGTH} и "
            f"не более {self.MAX_LENGTH} символов. "
            f"Разрешено использовать кириллицу, латиницу, "
            f"цифры и спецсимволы <-+_.!?@#№$%^&*>"
        )


def validate_first_name_and_last_name_fields(value):
    """Validate the user's first and last name."""
    if re.search(r"[\d]", value) is not None:
        raise ValidationError("Нельзя использовать цифры!")
    if value.count("-") > 1 or value.count(" ") > 1:
        raise ValidationError("Нельзя использовать 2 знака <-> или два пробела!")

    unacceptable_simbols = "".join(set(re.sub(r"[a-zA-Zа-яА-Я- ]", "", value)))
    if unacceptable_simbols:
        raise ValidationError(
            "Нельзя использовать эти символы <{unacceptable_simbols}>".format(
                unacceptable_simbols=unacceptable_simbols
            )
        )


@deconstructible
class CustomEmailValidator:
    """Modified Django EmailValidator.

    Custom user_regex, domain_regex and excluded Punycode when validate domain_part.
    """

    message = _("Enter a valid email address.")
    code = "invalid"
    user_regex = _lazy_re_compile(
        r"^[0-9A-Z]+([-|_]?[0-9A-Z]+)*(\.[0-9A-Z]+([-|_]?[0-9A-Z]+)*)*$",
        re.IGNORECASE,
    )
    domain_regex = _lazy_re_compile(
        # max length for domain name labels is 63 characters per RFC 1034
        r"^((?:[A-Z0-9](?:(?!.*-{2,})[0-9A-Z-]{0,61}[A-Z0-9])?\.)+)(?:[A-Z0-9]{2,63}(?<!-))$",
        re.IGNORECASE,
    )
    literal_regex = _lazy_re_compile(
        # literal form, ipv4 or ipv6 address (SMTP 4.1.3)
        r"^\[([A-F0-9:.]+)\]$",
        re.IGNORECASE,
    )
    domain_allowlist = ["localhost"]

    def __init__(self, message=None, code=None, allowlist=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if allowlist is not None:
            self.domain_allowlist = allowlist

    def __call__(self, value):
        """Validate email."""
        if not value or "@" not in value:
            raise ValidationError(self.message, code=self.code, params={"value": value})

        user_part, domain_part = value.rsplit("@", 1)

        if not self.user_regex.match(user_part):
            raise ValidationError(self.message, code=self.code, params={"value": value})

        is_domain_part_valid = self.validate_domain_part(domain_part)
        is_domain_part_in_domain_allowlist = domain_part in self.domain_allowlist
        if not is_domain_part_in_domain_allowlist and not is_domain_part_valid:
            raise ValidationError(self.message, code=self.code, params={"value": value})

    def validate_domain_part(self, domain_part):
        """Validate domain part of email."""
        if self.domain_regex.match(domain_part):
            return True

        literal_match = self.literal_regex.match(domain_part)
        if literal_match:
            ip_address = literal_match[1]
            try:
                validate_ipv46_address(ip_address)
                return True
            except ValidationError:
                pass

        return False

    def __eq__(self, other):
        return (
            isinstance(other, EmailValidator)
            and (self.domain_allowlist == other.domain_allowlist)
            and (self.message == other.message)
            and (self.code == other.code)
        )
