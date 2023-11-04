import re

from django.conf import settings
from django.core.exceptions import ValidationError
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
        if len(symbol) > 0:
            raise ValidationError(_(f"Символы <{''.join(symbol)}> запрещены!"))

    def get_help_text(self):
        return _(
            "Ваш пароль должен содержать не менее %(min_length)d и не "
            "более %(max_length)d символов. Разрешено использовать латинский алфавит, "
            "цифры и спецсимволы <-+_.!?@#$%^&*>"
            % {"min_length": self.min_length, "max_length": self.max_length}
        )


def validate_first_name_and_last_name_fields(input_string):
    if re.search(r"[\d]", input_string) is not None:
        raise ValidationError("Нельзя использовать цифры!")
    if input_string.count("-") > 1 or input_string.count(" ") > 1:
        raise ValidationError("Нельзя использовать 2 знака <-> или два пробела!")
    symbol = set(input_string) - set(
        "".join(re.findall(r"[a-zA-Zа-яА-Я- ]", input_string))
    )
    if len(symbol) > 0:
        raise ValidationError("Нельзя использовать эти символы <{}>".format(*symbol))


def validate_email_field(email):
    patterns = {
        "[a-zA-Z0-9._-]+": email.split("@")[0],
        "[a-zA-Z0-9.-]+": email.split("@")[1].split(".")[0],
        "[a-zA-Z]{2,63}": email.split(".")[1],
    }
    exception = {
        "[a-zA-Z0-9._-]+": "f'До <@> нельзя использовать эти символы <{symbol}>'",
        "[a-zA-Z0-9.-]+": "f'От <@> до <.> нельзя использовать эти символы <{symbol}>'",
        "[a-zA-Z]{2,63}": "f'После <.> нельзя использовать эти символы <{symbol}>'",
    }

    lower_email = email.lower()
    if lower_email.startswith(("-", "_", ".")) or lower_email.endswith(("-", "_", ".")):
        raise ValidationError(
            "Адрес почты не должен начинаться или заканчиваться символами <-_.>!"
        )
    if email.count("@") > 1:
        raise ValidationError("Нельзя использовать 2 знака <@>!")
    for pattern in patterns:
        symbol = set(patterns[pattern]) - set(
            "".join(re.findall(pattern, patterns[pattern]))
        )
        if len(symbol) > 0:
            symbol = "".join(symbol)
            raise ValidationError(eval(exception[pattern]))
