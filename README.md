# Сервер Main приложения Octopus

## Описание


## Документация API

Статическая:

http://127.0.0.1:8008/api/redoc/v1/

http://127.0.0.1:8008/api/swagger/v1/

Динамическая:

http://127.0.0.1:8008/api/dynamic_doc/v1/download/

http://127.0.0.1:8008/api/redoc/v1/dynamic/

http://127.0.0.1:8008/api/swagger/v1/dynamic/


## Технологии

Python 3.11

Django 4.1

Django REST Framework 3.14.0

DRF-Spectacular 0.26.5

Simple JWT 5.3.0

PostgreSQL 16


## Запуск проекта

1. Установить сервер баз данных PostgreSQL версии 16 и выше ([документация](https://www.postgresql.org/))

2. Создать базу данных PostgreSQL

3. Cоздать и активировать виртуальное окружение:
```
py -3.11 -m venv venv (Windows)
python3 -m venv venv (Linux, MacOS)

source venv/Scripts/activate (Windows)
source venv/bin/activate (Linux, MacOS)
```

4. Обновить pip:
```
python -m pip install --upgrade pip
```

5. Установить зависимости:
```
pip install -r requirements.txt
```

6. Скопировать файл .env_sample и переименовать в .env. Установить значения параметров в файле:
```
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=<db name>
POSTGRES_USER=<postgres user>
POSTGRES_PASSWORD=<postgres password>
DB_HOST=<db host>
DB_PORT=<db port>

DJANGO_SECRET_KEY=<secret key>

ACCESS_TOKEN_LIFETIME=<seconds>
REFRESH_TOKEN_LIFETIME=<seconds>
```
7. Выполнить миграции:
```
python manage.py makemigrations

python manage.py migrate
```

8. Импортировать данные о компаниях из csv файла в БД
```
python manage.py import_data_companies
```

9. Дамп БД
```
python -Xutf8 ./manage.py dumpdata > ../data_companies.json
```

10. Импортировать данные о компаниях из json файла в БД
```
python manage.py loaddata ../data_companies.json
```

11. Создать суперпользователя:
```
python manage.py createsuperuser
```

12. Запустить проект:
```
python manage.py runserver 8008
```

## Команда проекта
