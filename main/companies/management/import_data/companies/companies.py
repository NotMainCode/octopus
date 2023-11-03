"""Function for importing test data about companies from csv file into the DB."""

from companies.management.import_data.core.csv_file_reader import get_data_from_csv_file
from companies.management.import_data.core.data_cleaners.file_fields import (
    download_files_and_save_upload_to_value,
)
from companies.management.import_data.core.data_cleaners.m2m_fields import (
    get_clean_data_for_m2m_field,
)
from companies.management.import_data.core.data_cleaners.m2o_fields import (
    get_clean_data_for_m2o_field,
)
from companies.management.import_data.core.data_cleaners.simple_fields import (
    remove_object_with_invalid_data,
)
from companies.management.import_data.core.fix_phone_number import fix_phone_number
from companies.management.import_data.core.messengers import (
    display_message_data_import_from_file_completed,
)
from companies.models import Company, Industry, Phone, Service


def import_data_companies(file_paths: dict[str, str]) -> None:
    """Import data about companies from csv file into DB."""
    companies = get_data_from_csv_file(file_paths["companies"])
    remove_object_with_invalid_data(companies, Company)

    download_files_and_save_upload_to_value(
        objects_csv_data=companies,
        objects_file_field_name="logo",
        objects_field_name_for_file_name="name",
        objects_model_name=Company,
    )

    industries = get_data_from_csv_file(file_paths["industries"])
    industries_of_all_companies = get_clean_data_for_m2m_field(
        objects_csv_data=companies,
        m2m_field_name="industries",
        m2m_objects_csv_data=industries,
        m2m_model=Industry,
        field_name_in_m2m_model="name",
    )

    services = get_data_from_csv_file(file_paths["services"])
    services_of_all_companies = get_clean_data_for_m2m_field(
        objects_csv_data=companies,
        m2m_field_name="services",
        m2m_objects_csv_data=services,
        m2m_model=Service,
        field_name_in_m2m_model="name",
    )

    phones_of_all_companies = get_clean_data_for_m2o_field(
        objects_csv_data=companies,
        m2o_field_name="phones",
        get_clean_value=fix_phone_number,
    )

    Company.objects.all().delete()
    companies_in_db = Company.objects.bulk_create(
        (Company(**company) for company in companies if company)
    )

    for company, industry_ids, service_ids, phone_numbers in zip(
        companies_in_db,
        industries_of_all_companies,
        services_of_all_companies,
        phones_of_all_companies,
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
            (Phone(company_id=company.id, number=number) for number in phone_numbers)
        )

    display_message_data_import_from_file_completed(file_paths["companies"])
