# Сервер Main приложения Octopus

## Описание


## Документация API

Статическая (reference):

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

DEBUG=<boolean>
DJANGO_SECRET_KEY=<secret key>
ALLOWED_HOSTS=<ip address> <domain name>
PASSWORD_RESET_TIMEOUT=<seconds> # confirmation link lifetime

ACCESS_TOKEN_LIFETIME=<seconds>
REFRESH_TOKEN_LIFETIME=<seconds>

EMAIL_HOST_USER = <email address>
EMAIL_HOST_PASSWORD = <email password>
EMAIL_USE_SSL=<boolean>
EMAIL_HOST=<mail server domain name>
EMAIL_PORT=<mail port>
FROM_EMAIL=<sender name>
```
7. Выполнить миграции:
```
python manage.py makemigrations

python manage.py migrate
```

8. Импортировать тестовые данные о компаниях
```
python manage.py loaddata ../test_data_companies.json

Содержимое папки 'test_data_companies_media' скопировать в папку 'main/media'
```

9. Создать суперпользователя:
```
python manage.py createsuperuser
```

10.Запустить проект:
```
python manage.py runserver 8008
```

## Команда проекта

[NotMainCode](https://github.com/NotMainCode)

[Stryukov](https://github.com/Stryukov)

[zemtsov-dm](https://github.com/zemtsov-dm)

[aleksandrkomyagin](https://github.com/aleksandrkomyagin)

[olees-orlenko](https://github.com/olees-orlenko)