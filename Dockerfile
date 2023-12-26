FROM python:3.11-slim as base
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY ./octopus/ .
COPY ./infra/build_scripts/wait-for-it.sh .
RUN chmod +x wait-for-it.sh
RUN python manage.py collectstatic --no-input

FROM base as prod
COPY ./infra/build_scripts/run_app.prod.sh .
RUN chmod +x run_app.prod.sh

FROM base as dev
COPY ./infra/build_scripts/run_app.dev.sh .
RUN chmod +x run_app.dev.sh
COPY ./db_test_data/media/ ./media/
COPY ./db_test_data/json_files/ .
