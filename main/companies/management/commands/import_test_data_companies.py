"""Django-admin command for import test data about companies from .csv files to DB."""

import csv
import os
from sys import stdout

import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from companies.models import Company, Industry, Phone, Service, ServiceCategory

FILENAMES = {
    "companies": "companies.csv",
    "industries": "industries.csv",
    "service_categories": "service_categories.csv",
    "services": "services.csv",
}

COUNT_PHONE_DIGITS = 11


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        import_data()
        self.stdout.write("Import of test data is completed.")


def import_data() -> None:
    import_data_industries(FILENAMES["industries"])
    import_data_service_categories(FILENAMES["service_categories"])
    import_data_services(FILENAMES["services"])
    import_data_companies(FILENAMES)


def import_data_industries(filename: str) -> None:
    industries = get_resource_data_from_file(filename)
    Industry.objects.all().delete()
    Industry.objects.bulk_create(
        (Industry(name=industry["name"]) for industry in industries)
    )
    display_message_successfull_import(filename)


def import_data_service_categories(filename: str) -> None:
    service_categories = get_resource_data_from_file(filename)
    ServiceCategory.objects.all().delete()
    ServiceCategory.objects.bulk_create(
        (ServiceCategory(**service_category) for service_category in service_categories)
    )
    display_message_successfull_import(filename)


def import_data_services(filename: str) -> None:
    services = get_resource_data_from_file(filename)
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
    display_message_successfull_import(filename)


def import_data_companies(filenames: dict[str, str]) -> None:
    companies = get_resource_data_from_file(filenames["companies"])
    company_numbers_to_remove = []
    for company_number, company in enumerate(companies):
        if not company["name"]:
            correct_number = company_number + 2
            stdout.write(
                f"Company № {correct_number} has no name or line {correct_number} is empty. "
                f"Company will not be saved.\n"
            )
            company_numbers_to_remove.append(company_number)
            continue

        try:
            int(company["year_founded"])
        except ValueError:
            correct_number = company_number + 2
            stdout.write(
                f"Company {correct_number} has incorrect "
                f"year_founded '{company['year_founded']}'. "
                f"Company will not be saved.\n"
            )
            company_numbers_to_remove.append(company_number)
            continue

        try:
            int(company["team_size"])
        except ValueError:
            correct_number = company_number + 2
            stdout.write(
                f"Company № {correct_number} has incorrect team_size '{company['team_size']}'. "
                f"Company will not be saved.\n"
            )
            company_numbers_to_remove.append(company_number)

    for company_number_to_remove in company_numbers_to_remove[::-1]:
        companies.pop(company_number_to_remove)

    industries = get_resource_data_from_file(filenames["industries"])
    industry_ids = {
        industry.name: industry_id
        for industry_id, industry in Industry.objects.in_bulk().items()
    }
    for industry in industries:
        industry["id"] = industry_ids[industry["name"]]
    industries_of_all_companies = [
        company.pop("industries").split("\n") for company in companies
    ]

    for company_industries in industries_of_all_companies:
        industry_numbers_to_remove = []
        for company_industry_number, company_industry in enumerate(company_industries):
            if not company_industry:
                industry_numbers_to_remove.append(company_industry_number)
                continue

            is_company_industry_correct = False
            for industry in industries:
                for industry_synonym in industry["synonyms"].split("\n"):
                    if company_industry.lower() == industry_synonym.lower():
                        company_industries[company_industry_number] = industry["id"]
                        is_company_industry_correct = True
                        break

            if not is_company_industry_correct:
                industry_numbers_to_remove.append(company_industry_number)
                stdout.write(
                    f"Unknown industry name '{company_industry}'. "
                    f"The company's industry will not be saved.\n"
                )

        for industry_number in industry_numbers_to_remove[::-1]:
            company_industries.pop(industry_number)

    services = get_resource_data_from_file(filenames["services"])
    services_ids = {
        service.name: service_id
        for service_id, service in Service.objects.in_bulk().items()
    }
    for service in services:
        service["id"] = services_ids[service["name"]]
    services_of_all_companies = [
        company.pop("services").split("\n") for company in companies
    ]

    for company_services in services_of_all_companies:
        service_numbers_to_remove = []
        for number, company_service in enumerate(company_services):
            if not company_service:
                service_numbers_to_remove.append(number)
                continue

            is_company_service_correct = False
            for service in services:
                for service_synonym in service["synonyms"].split("\n"):
                    if company_service.lower() == service_synonym.lower():
                        company_services[number] = service["id"]
                        is_company_service_correct = True
                        break

            if not is_company_service_correct:
                service_numbers_to_remove.append(number)
                stdout.write(
                    f"Unknown service name '{company_service}'. "
                    f"The company's service will not be saved.\n"
                )

        for service_number in service_numbers_to_remove[::-1]:
            company_services.pop(service_number)

    phones_of_all_companies = [
        company.pop("phones").split("\n") for company in companies
    ]
    for company_phones in phones_of_all_companies:
        item_numbers_to_remove = []
        for item_number, phone in enumerate(company_phones):
            phone_digits = "".join(filter(str.isdigit, phone))
            if len(phone_digits) == COUNT_PHONE_DIGITS:
                if phone_digits[0] in {"7", "8"}:
                    company_phones[item_number] = "+7 ({}) {}-{}-{}".format(
                        phone_digits[1:4],
                        phone_digits[4:7],
                        phone_digits[7:9],
                        phone_digits[9:11],
                    )
                    continue

            item_numbers_to_remove.append(item_number)
            stdout.write(
                f"Incorrect phone number '{phone}'. "
                f"The phone number of company will not be saved.\n"
            )

        for item_number in item_numbers_to_remove[::-1]:
            company_phones.pop(item_number)

    logos_of_all_companies = [company.pop("logo") for company in companies]

    Company.objects.all().delete()
    companies_in_db = Company.objects.bulk_create(
        (Company(**company) for company in companies if company)
    )

    for company, industry_ids, service_ids, phones, logo_url in zip(
        companies_in_db,
        industries_of_all_companies,
        services_of_all_companies,
        phones_of_all_companies,
        logos_of_all_companies,
    ):
        Company.industries.through.objects.bulk_create(
            (
                Company.industries.through(
                    company_id=company.id, industry_id=industry_id
                )
                for industry_id in industry_ids
            )
        )
        Company.services.through.objects.bulk_create(
            (
                Company.services.through(company_id=company.id, service_id=service_id)
                for service_id in service_ids
            )
        )
        Phone.objects.bulk_create(
            (Phone(company_id=company.id, phone=phone) for phone in phones)
        )

        try:
            file_name = "".join(
                (
                    "".join(filter(str.isalpha, company.name)),
                    logo_url[logo_url.rindex(".", -5) :],
                )
            )
        except ValueError:
            continue

        logo_field_value = os.path.join(
            Company._meta.get_field("logo").upload_to, file_name
        )
        file_path = os.path.join(settings.MEDIA_ROOT, logo_field_value)

        if not os.path.isfile(file_path):
            try:
                response = requests.get(logo_url)
            except requests.exceptions.ConnectTimeout:
                stdout.write(
                    f"Failed to download the '{company.name}' company logo "
                    f"from the link {logo_url}\n"
                )
                continue

            try:
                open(file_path, "wb").write(response.content)
            except IOError:
                stdout.write(
                    f"Failed to save the '{company.name}' company logo file "
                    f"downloaded from the link {logo_url}\n"
                )
                continue

        company.logo = logo_field_value

    Company.objects.bulk_update(companies_in_db, ["logo"])


def get_resource_data_from_file(filename: str) -> list[dict[str, str]]:
    try:
        file = open(
            os.path.join(settings.BASE_DIR, "db_test_data/companies", filename),
            "r",
            encoding="utf8",
        )
    except IOError:
        raise CommandError(f"File {filename} open error.")

    resource_data = list(csv.DictReader(file, delimiter=";"))
    file.close()

    return resource_data


def display_message_successfull_import(filename) -> None:
    stdout.write(
        f"Data from the file `{filename}` has been imported into the database.\n"
    )
