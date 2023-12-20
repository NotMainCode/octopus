"""Convert phone number format to +7 (XXX) XXX-XX-XX."""

from applications.companies.management.import_data.companies.constants import (
    COUNT_PHONE_DIGITS,
)


def fix_phone_number(value: str) -> str | None:
    """Convert phone number format to +7 (XXX) XXX-XX-XX."""
    phone_digits = "".join(filter(str.isdigit, value))
    if len(phone_digits) == COUNT_PHONE_DIGITS:
        if phone_digits[0] in {"7", "8"}:
            return "+7 ({}) {}-{}-{}".format(
                phone_digits[1:4],
                phone_digits[4:7],
                phone_digits[7:9],
                phone_digits[9:11],
            )

    return None
