"""Validators for User model fields."""

import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, validate_ipv46_address
from django.utils.deconstruct import deconstructible
from django.utils.regex_helper import _lazy_re_compile
from django.utils.translation import gettext as _


class CustomPasswordValidator:
    def __init__(
        self,
        min_length=settings.MIN_LEN_PASSWORD_USER_MODEL,
        max_length=settings.MAX_LEN_PASSWORD_USER_MODEL,
    ):
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, password, user=None):
        if not password:
            return
        if len(password) < self.min_length:
            raise ValidationError(
                _("Минимальная длина пароля %(min_length)d символов!"),
                code="Короткий пароль!",
                params={"min_length": self.min_length},
            )

        if len(password) > self.max_length:
            raise ValidationError(
                _("Максимальная длина пароля %(max_length)d символов!"),
                code="Длинный пароль!",
                params={"max_length": self.max_length},
            )

        if re.search(r"[^0-9]", password) is None:
            raise ValidationError(_("Пароль не должен содержать только цифры!"))
        pattern = r"[a-zA-Zа-яА-Я-+_.!?@#$%^&*\d+=/]"
        symbol = set(password) - set("".join(re.findall(pattern, password)))
        if symbol:
            raise ValidationError(_(f"Символы <{''.join(symbol)}> запрещены!"))

    def get_help_text(self):
        return _(
            f"Ваш пароль должен содержать не менее {self.min_length} и "
            f"не более {self.max_length} символов. "
            f"Разрешено использовать латинский алфавит, "
            f"цифры и спецсимволы <-+_.!?@#$%^&*>"
        )


def validate_first_name_and_last_name_fields(input_string):
    if re.search(r"[\d]", input_string) is not None:
        raise ValidationError("Нельзя использовать цифры!")
    if input_string.count("-") > 1 or input_string.count(" ") > 1:
        raise ValidationError("Нельзя использовать 2 знака <-> или два пробела!")
    symbol = set(input_string) - set(
        "".join(re.findall(r"[a-zA-Zа-яА-Я- ]", input_string))
    )
    if symbol:
        raise ValidationError("Нельзя использовать эти символы <{}>".format(*symbol))


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
        if not value or "@" not in value:
            raise ValidationError(self.message, code=self.code, params={"value": value})

        user_part, domain_part = value.rsplit("@", 1)

        if not self.user_regex.match(user_part):
            raise ValidationError(self.message, code=self.code, params={"value": value})

        if domain_part not in self.domain_allowlist and not self.validate_domain_part(
            domain_part
        ):
            raise ValidationError(self.message, code=self.code, params={"value": value})

    def validate_domain_part(self, domain_part):
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
