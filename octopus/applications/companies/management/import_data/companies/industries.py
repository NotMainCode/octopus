"""Function for importing test data about industries from csv file into the DB."""

from applications.companies.management.import_data.core.csv_file_reader import (
    get_data_from_csv_file,
)
from applications.companies.management.import_data.core.messengers import (
    display_message_data_import_from_file_completed,
)
from applications.companies.models import Industry


def import_data_industries(file_path: str) -> None:
    """Import test data about industries from csv file into the DB."""
    industries = get_data_from_csv_file(file_path)
    Industry.objects.all().delete()
    Industry.objects.bulk_create(
        (Industry(name=industry["name"]) for industry in industries)
    )
    display_message_data_import_from_file_completed(file_path)
