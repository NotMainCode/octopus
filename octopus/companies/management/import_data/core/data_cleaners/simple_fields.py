"""Validate CSV data for simple fields (non-M2M and non-M2O) and remove invalid data."""

from django.core.exceptions import ValidationError
from django.db import models

from companies.management.import_data.core.messengers import (
    display_message_empty_required_field,
    display_message_invalid_field_value,
)


def remove_object_with_invalid_data(
    objects_csv_data: list[dict[str, str | int]], model: models.base.ModelBase
) -> None:
    """Remove objects with invalid data."""
    (
        field_validators,
        required_fields,
        integer_type_fields,
    ) = get_field_validators_required_fields_int_type_fields(model)

    for object_index in range(len(objects_csv_data) - 1, -1, -1):
        for field_name in objects_csv_data[object_index].keys():
            if remove_object_with_empty_required_field(
                objects_csv_data, object_index, field_name, required_fields
            ):
                break

            if field_name in integer_type_fields:
                if remove_object_with_failed_str_to_int(
                    objects_csv_data, object_index, field_name
                ):
                    break

            if remove_object_with_invalid_field_value(
                objects_csv_data, object_index, field_name, field_validators[field_name]
            ):
                break


def get_field_validators_required_fields_int_type_fields(
    model: models.base.ModelBase,
) -> tuple[dict[str, list], set[str], set[str]]:
    """Get field validators, required field names and integer type field names."""
    field_validators = {}
    required_fields = set()
    integer_type_fields = set()

    for field in model._meta.get_fields():
        try:
            field_validators[field.name] = field.validators
        except AttributeError:
            field_validators[field.name] = ()

        if (
            not issubclass(field.__class__, models.ManyToManyField)
            and not field.null
            and not field.blank
        ):
            required_fields.add(field.name)

        if issubclass(field.__class__, models.IntegerField):
            integer_type_fields.add(field.name)

    return field_validators, required_fields, integer_type_fields


def remove_object_with_empty_required_field(
    objects_csv_data: list[dict[str, str]],
    object_index: int,
    field_name: str,
    required_fields: set[str],
) -> bool:
    """Remove object with empty required field."""
    field_value = objects_csv_data[object_index][field_name]
    if not field_value and field_name in required_fields:
        objects_csv_data.pop(object_index)
        object_number = object_index + 1
        display_message_empty_required_field(object_number, field_name)
        return True

    return False


def remove_object_with_failed_str_to_int(
    objects_csv_data: list[dict[str, str | int]], object_index: int, field_name: str
) -> bool:
    """Remove object with failed conversion of a string data value to an integer."""
    field_value = objects_csv_data[object_index][field_name]
    try:
        objects_csv_data[object_index][field_name] = int(field_value)
    except ValueError as exc:
        object_number = object_index + 1
        display_message_invalid_field_value(object_number, field_name, field_value, exc)
        objects_csv_data.pop(object_index)
        return True

    return False


def remove_object_with_invalid_field_value(
    objects_csv_data: list[dict[str, str]],
    object_index: int,
    field_name: str,
    validators,
) -> bool:
    """Remove object with invalid field value."""
    field_value = objects_csv_data[object_index][field_name]
    for validator in validators:
        try:
            validator(field_value)
        except ValidationError as exc:
            object_number = object_index + 1
            display_message_invalid_field_value(
                object_number, field_name, field_value, exc
            )
            objects_csv_data.pop(object_index)
            return True

    return False
