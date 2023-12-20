"""Function for importing test data about service categories from csv file into the DB."""

from applications.companies.management.import_data.core.csv_file_reader import (
    get_data_from_csv_file,
)
from applications.companies.management.import_data.core.messengers import (
    display_message_data_import_from_file_completed,
)
from applications.companies.models import ServiceCategory


def import_data_service_categories(file_path: str) -> None:
    """Import test data about service categories from csv file into the DB."""
    service_categories = get_data_from_csv_file(file_path)
    ServiceCategory.objects.all().delete()
    ServiceCategory.objects.bulk_create(
        (ServiceCategory(**service_category) for service_category in service_categories)
    )
    display_message_data_import_from_file_completed(file_path)
