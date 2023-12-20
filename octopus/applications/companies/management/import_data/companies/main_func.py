"""Main function for import test data about companies from .csv files to DB."""

from applications.companies.management.import_data.companies.companies import (
    import_data_companies,
)
from applications.companies.management.import_data.companies.constants import FILE_PATHS
from applications.companies.management.import_data.companies.industries import (
    import_data_industries,
)
from applications.companies.management.import_data.companies.service_categories import (
    import_data_service_categories,
)
from applications.companies.management.import_data.companies.services import (
    import_data_services,
)


def import_data_main_func() -> None:
    """Import test data about companies from .csv files to DB."""
    import_data_industries(FILE_PATHS["industries"])
    import_data_service_categories(FILE_PATHS["service_categories"])
    import_data_services(FILE_PATHS["services"])
    import_data_companies(FILE_PATHS)
