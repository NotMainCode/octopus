"""Message display functions."""

from sys import stdout

from django.core.exceptions import ValidationError


def display_message_data_import_from_file_completed(filename) -> None:
    """Display a message about the completion of importing data from the file."""
    stdout.write(
        f"Data from the file `{filename}` has been imported into the database.\n"
    )


def display_message_failed_to_download_file_from_url(url: str) -> None:
    """Display message that file could not be downloaded from url."""
    stdout.write(f"Failed to download file from url {url}\n.")


def display_message_failed_save_file_from_url(url: str) -> None:
    """Display message that file downloaded from url could not be saved."""
    stdout.write(f"Failed to save file downloaded from {url}.\n")


def display_message_no_file_extension_in_url(url: str) -> None:
    """Display message that url does not contain file extension."""
    stdout.write(
        f"URL does not contain file extension.\n{url}\nThe file will not be saved.\n"
    )


def display_message_empty_required_field(object_number: int, field_name: str) -> None:
    """Display message about object with empty required field."""
    stdout.write(
        f"Object № {object_number} is missing a value "
        f"for the required '{field_name}' field. Object will not be saved.\n"
    )


def display_message_invalid_field_value(
    object_number: int,
    field: str,
    field_value: str,
    exc: ValidationError | ValueError,
) -> None:
    """Display message about object with invalid field value."""
    stdout.write(
        f"Object № {object_number} has invalid {field} '{field_value}'. "
        f"Additional info: {exc}. "
        f"Object will not be saved.\n"
    )


def display_message_invalid_data_for_m2m_m2o_field(
    m2m_field_name: str, m2m_field_value: str
):
    """Display message about invalid data for field in m2m table."""
    stdout.write(
        f"Unknown value for the '{m2m_field_name}' field '{m2m_field_value}'. "
        f"The value will not be saved.\n"
    )
