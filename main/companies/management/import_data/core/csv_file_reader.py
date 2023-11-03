"""Function for reading data from a csv file."""

import csv

from django.core.management import CommandError


def get_data_from_csv_file(file_path: str) -> list[dict[str, str]]:
    """Get data from csv file."""
    try:
        file = open(file_path, "r", encoding="utf8")
    except IOError:
        raise CommandError(f"File {file_path} open error.")

    resource_data = list(csv.DictReader(file, delimiter=";"))
    file.close()

    return resource_data
