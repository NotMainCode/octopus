"""Function for importing test data about services from csv file into the DB."""

from companies.management.import_data.core.csv_file_reader import get_data_from_csv_file
from companies.management.import_data.core.messengers import (
    display_message_data_import_from_file_completed,
)
from companies.models import Service, ServiceCategory


def import_data_services(file_path: str) -> None:
    """Import test data about services from csv file into the DB."""
    services = get_data_from_csv_file(file_path)
    service_category_ids = {
        service.name: service_id
        for service_id, service in ServiceCategory.objects.in_bulk().items()
    }

    Service.objects.bulk_create(
        (
            Service(
                category_id=service_category_ids[service["category"]],
                name=service["name"],
            )
            for service in services
        )
    )
    display_message_data_import_from_file_completed(file_path)
