"""Download files and prepare the data to be saved in the database."""

import os

import requests
from django.conf import settings
from django.db import models

from companies.management.import_data.core.messengers import (
    display_message_failed_save_file_from_url,
    display_message_failed_to_download_file_from_url,
    display_message_no_file_extension_in_url,
)


def download_files_and_save_upload_to_value(
    objects_csv_data: list[dict[str, str | int]],
    objects_file_field_name: str,
    objects_field_name_for_file_name: str,
    objects_model_name: models.base.ModelBase,
) -> None:
    """Download and save the file, prepare the data to be saved in the database."""
    upload_to = objects_model_name._meta.get_field(objects_file_field_name).upload_to

    for object_csv_data in objects_csv_data:
        file_url = object_csv_data[objects_file_field_name]
        try:
            file_name = "".join(
                (
                    "".join(
                        filter(
                            str.isalpha,
                            object_csv_data[objects_field_name_for_file_name],
                        )
                    ),
                    file_url[file_url.rindex(".", -5) :],
                )
            )
        except ValueError:
            display_message_no_file_extension_in_url(file_url)
            object_csv_data[objects_file_field_name] = ""
            continue

        file_field_value = os.path.join(upload_to, file_name)
        file_path = os.path.join(settings.MEDIA_ROOT, file_field_value)

        try:
            response = requests.get(file_url)
        except requests.exceptions.ConnectTimeout:
            display_message_failed_to_download_file_from_url(file_url)
            object_csv_data[objects_file_field_name] = ""
            continue

        try:
            open(file_path, "wb").write(response.content)
        except IOError:
            display_message_failed_save_file_from_url(file_url)
            object_csv_data[objects_file_field_name] = ""
            continue

        object_csv_data[objects_file_field_name] = file_field_value
