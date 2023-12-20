"""Django-admin command for import test data about companies from .csv files into DB."""

from django.core.management.base import BaseCommand

from applications.companies.management.import_data.companies.main_func import (
    import_data_main_func,
)


class Command(BaseCommand):
    """import test data about companies from .csv files into DB."""

    def handle(self, *args, **options) -> None:
        import_data_main_func()
        self.stdout.write("Data import is completed.")
