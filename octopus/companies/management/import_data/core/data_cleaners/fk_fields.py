from django.db import models


def set_fk_fields_values(
    objects_csv_data: list[dict[str, str | int]],
    fk_field_name: str,
    fk_model: models.base.ModelBase,
    field_name_in_fk_model: str,
) -> None:
    csv_data_for_fk_model_field = {
        object_csv_data[fk_field_name] for object_csv_data in objects_csv_data
    }

    fk_model.objects.all().delete()
    fk_objects_in_db = fk_model.objects.bulk_create(
        (
            fk_model(**{field_name_in_fk_model: field_value_in_fk_model})
            for field_value_in_fk_model in csv_data_for_fk_model_field
        )
    )

    fk_objects = {
        getattr(fk_object_in_db, field_name_in_fk_model): fk_object_in_db
        for fk_object_in_db in fk_objects_in_db
    }

    for object_csv_data in objects_csv_data:
        object_csv_data[fk_field_name] = fk_objects[object_csv_data[fk_field_name]]
