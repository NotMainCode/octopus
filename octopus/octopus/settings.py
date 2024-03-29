import os
from datetime import timedelta
from pathlib import Path

from corsheaders.defaults import default_headers
from dotenv import load_dotenv

from core.time_in_seconds import TIME_IN_SECONDS

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-3zby_h+fe&7@xfqa+(4w$&wpuj&avz!fza910up8=z2409oak5",
)

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost 127.0.0.1").split(" ")

INTERNAL_IPS = ["127.0.0.1"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    "corsheaders",
    "applications.users",
    "applications.companies",
    "applications.api",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "octopus.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates/api_doc")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "octopus.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.postgresql"),
        "NAME": os.getenv("POSTGRES_DB", "postgres"),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "applications.users.validators.CustomPasswordValidator"}
]

AUTH_USER_MODEL = "users.User"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static/api_doc/")]

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        seconds=int(os.getenv("ACCESS_TOKEN_LIFETIME", TIME_IN_SECONDS["one_week"]))
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        seconds=int(os.getenv("REFRESH_TOKEN_LIFETIME", TIME_IN_SECONDS["one_week"]))
    ),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "ROTATE_REFRESH_TOKENS": True,
}

PASSWORD_RESET_TIMEOUT = int(
    os.getenv("PASSWORD_RESET_TIMEOUT", TIME_IN_SECONDS["one_week"])
)

EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "True") == "True"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.getenv("EMAIL_PORT", 465)
DEFAULT_FROM_EMAIL = os.getenv("FROM_EMAIL", EMAIL_HOST_USER)

CSRF_TRUSTED_ORIGINS = os.getenv(
    "CSRF_TRUSTED_ORIGINS", "http://localhost http://127.0.0.1"
).split(" ")

if DEBUG:
    INSTALLED_APPS.extend(["debug_toolbar", "drf_spectacular"])
    MIDDLEWARE.extend(["debug_toolbar.middleware.DebugToolbarMiddleware"])
    REST_FRAMEWORK.update(
        {
            "DEFAULT_AUTHENTICATION_CLASSES": [
                "rest_framework_simplejwt.authentication.JWTAuthentication",
                "rest_framework.authentication.SessionAuthentication",
            ],
            "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
        }
    )
    LOGIN_REDIRECT_URL = "/api/v1/companies/"
    SPECTACULAR_SETTINGS = {
        "TITLE": "Octopus API",
        "VERSION": "1.0.0",
        "SERVE_INCLUDE_SCHEMA": False,
    }
    CORS_ALLOWED_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]
    CORS_URLS_REGEX = r"^/api/.*$"
    CORS_ALLOW_HEADERS = [*default_headers, "x-xsrf-token"]
