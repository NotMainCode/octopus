FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./octopus/ .

COPY ./test_data_companies_media/ ./media/

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main.wsgi"]