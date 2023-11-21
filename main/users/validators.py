import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
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


class CustomEmailValidator(EmailValidator):
    """Django EmailValidator with custom user_regex."""

    user_regex = _lazy_re_compile(
        r"(^[-_0-9A-Z]+(\.[-_0-9A-Z]+)*\Z",
        re.IGNORECASE,
    )
