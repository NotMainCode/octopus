## Octopus API

## Оглавление
- [Описание](#описание)
- [Технологии](#технологии)
- [Запуск](#запуск)


## Описание

Octopus - это онлайн-платформа, которая предоставляет информацию об IT компаниях.

Добавление информации о компаниях возможно на сайте администратора, 
так же как и управление другими ресурсами (специализации и услуги компаний, пользователи и т.д.).

API Octopus предоставляет следующие возможности:
- регистрация пользователя с подтверждением по ссылке в email,
- авторизованные пользователи могут добавлять компании в избранное,
- получение списков городов, компаний, специализаций и услуг компаний,
- получение подробной информации о компании.

Проект временно доступен по ссылкам:
- [Сайт администратора](http://94.142.142.16/admin)
- Документация API: [redoc](http://94.142.142.16/api/redoc/v1/) и [swagger](http://94.142.142.16/api/swagger/v1/)
- Octopus API - http://94.142.142.16/api/v1/...

## Технологии
<details>
<summary>развернуть</summary>

Python 3.11

Django 4.1

Django REST Framework 3.14.0

DRF-Spectacular 0.26.5

Simple JWT 5.3.0

PostgreSQL 16

[⬆️В начало](#оглавление)
</details>


## Запуск
<details>
<summary>локально</summary>

1. Установить сервер баз данных PostgreSQL версии 16 и выше ([документация](https://www.postgresql.org/))

2. Создать базу данных PostgreSQL

3. Создать и активировать виртуальное окружение:
    ```bash
    py -3.11 -m venv venv (Windows)
    python3 -m venv venv (Linux, MacOS)
    
    source venv/Scripts/activate (Windows)
    source venv/bin/activate (Linux, MacOS)
    ```

4. Обновить pip:
    ```bash
    python -m pip install --upgrade pip
    ```

5. Установить зависимости:
    ```bash
    pip install -r requirements.txt
    ```

6. Скопировать файл `.env_sample_local` и переименовать в `.env`. 
Установить значения параметров в файле `.env`.

7. Выполнить миграции:
    ```bash
    python manage.py makemigrations
    
    python manage.py migrate
    ```

8. Тестовые данные о компаниях
   - Использовать csv файлы (находятся в папке `db_test_data/csv_files/companies/`)
       - Импортировать данные в БД 
         ```bash
         python manage.py import_data_companies
         ```

       - Сохранить данные в json файле
         ```bash
         python -Xutf8 manage.py dumpdata > companies.json
         ```

   - Использовать json файл с тестовыми данными о компаниях
       - Импортировать данные в БД
         ```bash
         python manage.py loaddata ../db_test_data/json_files/companies.json
         ```
      
       - Содержимое папки `db_test_data/media/` скопировать в папку `media/`


9. Создать суперпользователя:
    - интерактивно
        ```bash
        python manage.py createsuperuser
        ```

    - импортировать данные суперпользователя из json файла
        ```bash
        python manage.py loaddata ../db_test_data/json_files/users.json
        ```
      
      данные суперпользователя:
      - email - su@su.su
      - пароль - password


10. Запустить проект:
    ```bash
    python manage.py runserver 8008
    ```

После запуска проект доступен по адресам:
- сайт администратора
    ```markdown
    http://127.0.0.1:8008/admin/
    ```

- статическая документация API
    ```markdown
    http://127.0.0.1:8008/api/redoc/v1/
    
    http://127.0.0.1:8008/api/swagger/v1/
    ```

- динамическая документация API 
(генерируется библиотекой drf-spectacular, доступна при DEBUG=True):
    ```markdown
    http://127.0.0.1:8008/api/dynamic_doc/v1/download/
    
    http://127.0.0.1:8008/api/redoc/v1/dynamic/
    
    http://127.0.0.1:8008/api/swagger/v1/dynamic/
    ```

- Octopus API
    ```markdown
    http://127.0.0.1:8008/api/v1/...
    ```

[⬆️В начало](#оглавление)
</details>

<details>
<summary>локально в контейнерах</summary>

1. Для локального запуска в контейнерах необходимо наличие [Docker](https://docs.docker.com/get-docker/)
2. Скопировать файл `.env_sample_local` и переименовать в `.env`. 
Установить значения параметров в файле `.env`.
3. Перейти в папку `infra/compose_files/` и выполнить:
    ```shell
    docker compose -f docker-compose.build.dev.yml up -d
    ```

В БД будут загружены тестовые данные о компаниях и данные суперпользователя:
- email - su@su.su
- пароль - password

После запуска проект доступен по адресам:
- сайт администратора
    ```markdown
    http://localhost/admin
    ```

- статическая документация API
    ```markdown
    http://localhost/api/redoc/v1/
    
    http://localhost/api/swagger/v1/
    ```

- динамическая документация API 
(генерируется библиотекой drf-spectacular, доступна при DEBUG=True):
    ```markdown
    http://localhost/api/dynamic_doc/v1/download/
    
    http://localhost/api/redoc/v1/dynamic/
    
    http://localhost/api/swagger/v1/dynamic/
    ```

- Octopus API
    ```markdown
    http://localhost/api/v1/...
    ```

[⬆️В начало](#оглавление)
</details>

<details>
<summary>на удалённом сервере</summary>

1. Скопировать на сервер содержимое папки `infra/` кроме папки `scripts/`
    ```shell
    scp -r <path_to_folder>/compose_files <username>@<server_pub_ip>:/<path_to_folder>/octopus
    scp <path_to_file>/nginx.conf <username>@<server_pub_ip>:/<path_to_folder>/octopus
    scp <path_to_file>/.env_sample_remote <username>@<server_pub_ip>:/<path_to_folder>/octopus
    ```

2. Подключиться к серверу
    ```shell
    ssh <username>@<server_ip>
    ```

3. Переименовать файл `.env_sample_remote` в `.env`
    ```shell
    mv <path_to_file>/.env_sample_remote <path_to_file>/.env
    ```

4. Открыть файл `.env` и задать значения параметров
    ```shell
    nano <path_to_file>/.env
    ```

5. Установить [Docker Engine](https://docs.docker.com/engine/install/ubuntu/)
и [плагин Compose](https://docs.docker.com/compose/install/linux/#install-the-plugin-manually).
Выполнить [действия после установки Linux для Docker Engine](https://docs.docker.com/engine/install/linux-postinstall/).

6. Перейти в папку `compose_files/`
    ```shell
    cd <path_to_folder>/compose_files
    ```

7. Выполнить
   - для запуска сервера с тестовыми данными в БД
      ```shell
      docker compose -f docker-compose.dev.yml up -d
      ```

   - для запуска сервера без тестовых данных в БД
      ```shell
      docker compose -f docker-compose.prod.yml up -d
      ```

После запуска проект доступен по адресам:
- сайт администратора
    ```markdown
    http://<server_ip>/admin
    ```

- документация API
    ```markdown
    http://<server_ip>/api/redoc/v1/
    
    http://<server_ip>/api/swagger/v1/
    ```

- Octopus API
    ```markdown
    http://<server_ip>/api/v1/...
    ```

[⬆️В начало](#оглавление)
</details>
