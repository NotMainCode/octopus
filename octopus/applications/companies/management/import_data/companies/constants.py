"""Constants for use in logic of 'import_data_companies' django-admin commands."""

import os

from django.conf import settings

PATH_TO_CSV_FILES = os.path.join(
    settings.BASE_DIR.parent, "db_test_data/csv_files/companies"
)

FILE_PATHS = {
    "companies": os.path.join(PATH_TO_CSV_FILES, "companies.csv"),
    "industries": os.path.join(PATH_TO_CSV_FILES, "industries.csv"),
    "service_categories": os.path.join(PATH_TO_CSV_FILES, "service_categories.csv"),
    "services": os.path.join(PATH_TO_CSV_FILES, "services.csv"),
}

COUNT_PHONE_DIGITS = 11
