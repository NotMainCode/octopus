"""Validate CSV data for M2O fields, remove or correct invalid data."""

from typing import Callable

from applications.companies.management.import_data.core.messengers import (
    display_message_invalid_data_for_m2m_m2o_field,
)


def get_clean_data_for_m2o_field(
    objects_csv_data: list[dict[str, str | int]],
    m2o_field_name: str,
    get_clean_value: Callable,
):
    """Get clean data for M2M field."""
    field_values_of_objects = [
        object_csv_data.pop(m2o_field_name).split("\n")
        for object_csv_data in objects_csv_data
    ]

    for field_values_of_object in field_values_of_objects:
        start_index = len(field_values_of_object) - 1
        for index in range(start_index, -1, -1):
            if not field_values_of_object[index]:
                field_values_of_object.pop(index)
                continue

            clean_value = get_clean_value(field_values_of_object[index])
            if clean_value is None:
                display_message_invalid_data_for_m2m_m2o_field(
                    m2o_field_name, field_values_of_object[index]
                )
                field_values_of_object.pop(index)
                continue

            field_values_of_object[index] = clean_value

    return field_values_of_objects
