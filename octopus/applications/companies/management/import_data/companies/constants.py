"""Constants for use in logic of 'import_data_companies' django-admin commands."""

import os

from django.conf import settings

PATH_TO_DATA_FILES_DIR = os.path.join(
    settings.BASE_DIR, "db_test_data/csv_files/companies"
)

FILE_PATHS = {
    "companies": os.path.join(PATH_TO_DATA_FILES_DIR, "companies.csv"),
    "industries": os.path.join(PATH_TO_DATA_FILES_DIR, "industries.csv"),
    "service_categories": os.path.join(
        PATH_TO_DATA_FILES_DIR, "service_categories.csv"
    ),
    "services": os.path.join(PATH_TO_DATA_FILES_DIR, "services.csv"),
}

COUNT_PHONE_DIGITS = 11
