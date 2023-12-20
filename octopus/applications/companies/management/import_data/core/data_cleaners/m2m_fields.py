"""Validate CSV data for M2M fields, remove invalid data, replace str with id."""

from django.db import models

from applications.companies.management.import_data.core.messengers import (
    display_message_invalid_data_for_m2m_m2o_field,
)


def get_clean_data_for_m2m_field(
    objects_csv_data: list[dict[str, str | int]],
    m2m_field_name: str,
    m2m_objects_csv_data: list[dict[str, str]],
    m2m_model: models.base.ModelBase,
    field_name_in_m2m_model: str,
):
    """Get clean data for M2M field."""
    add_id_of_m2m_resource_to_m2m_objects_csv_data(
        m2m_objects_csv_data, m2m_model, field_name_in_m2m_model
    )

    field_values_of_objects = [
        object_csv_data.pop(m2m_field_name).split("\n")
        for object_csv_data in objects_csv_data
    ]

    for field_values_of_object in field_values_of_objects:
        start_index = len(field_values_of_object) - 1
        for index in range(start_index, -1, -1):
            if not field_values_of_object[index]:
                field_values_of_object.pop(index)
                continue

            replace_m2m_field_value_with_id(
                m2m_objects_csv_data,
                field_values_of_object,
                index,
                m2m_field_name,
            )

    return field_values_of_objects


def add_id_of_m2m_resource_to_m2m_objects_csv_data(
    m2m_objects_csv_data: list[dict[str, str | int]],
    m2m_model: models.base.ModelBase,
    field_name_in_m2m_model: str,
) -> None:
    """Add id of M2M resource in DB to M2M objects csv data."""
    m2m_resource_in_db_ids = get_mapping_resource_field_name_to_resource_id(
        m2m_model, field_name_in_m2m_model
    )
    for m2m_object_csv_data in m2m_objects_csv_data:
        m2m_object_csv_data["id"] = m2m_resource_in_db_ids[
            m2m_object_csv_data[field_name_in_m2m_model]
        ]


def get_mapping_resource_field_name_to_resource_id(
    model: models.base.ModelBase, field_name: str
) -> dict[str, int]:
    """Get mapping resource field name to resource id."""
    return {
        getattr(m2m_resource_in_db, field_name): m2m_resource_in_db_id
        for m2m_resource_in_db_id, m2m_resource_in_db in model.objects.in_bulk().items()
    }


def replace_m2m_field_value_with_id(
    m2m_objects_csv_data: list[dict[str, str | int]],
    field_values_of_object: list[str],
    index: int,
    m2m_field_name,
) -> None:
    """Replace M2M field value with id."""
    for m2m_object_csv_data in m2m_objects_csv_data:
        for m2m_field_value_synonym in m2m_object_csv_data["synonyms"].split("\n"):
            if field_values_of_object[index].lower() == m2m_field_value_synonym.lower():
                field_values_of_object[index] = m2m_object_csv_data["id"]
                return

    display_message_invalid_data_for_m2m_m2o_field(
        m2m_field_name=m2m_field_name,
        m2m_field_value=field_values_of_object[index],
    )
    field_values_of_object.pop(index)
