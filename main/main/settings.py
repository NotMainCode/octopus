import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-3zby_h+fe&7@xfqa+(4w$&wpuj&avz!fza910up8=z2409oak5",
)

DEBUG = True

ALLOWED_HOSTS = []

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
    "users",
    "companies",
    "api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "main.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "main.wsgi.application"

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
    {
        "NAME": "users.validators.CustomPasswordValidator",
    },
]

AUTH_USER_MODEL = "users.User"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/django/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication"
    ],
}

ONE_WEEK_IN_SECONDS = 604800

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        seconds=int(os.getenv("ACCESS_TOKEN_LIFETIME", ONE_WEEK_IN_SECONDS))
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        seconds=int(os.getenv("REFRESH_TOKEN_LIFETIME", ONE_WEEK_IN_SECONDS))
    ),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
}

PASSWORD_RESET_TIMEOUT = int(os.getenv("PASSWORD_RESET_TIMEOUT", 86400))

# CONSTANTS
MAX_LEN_FULL_NAME_USER_MODEL: int = 30
MAX_LEN_EMAIL_USER_MODEL: int = 254
MIN_LEN_PASSWORD_USER_MODEL: int = 8
MAX_LEN_PASSWORD_USER_MODEL: int = 30
MAX_LEN_HASH_PASSWORD_USER_MODEL: int = 128

# EMAIL
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_SSL = True
EMAIL_HOST = "smtp.rambler.ru"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 465

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
    SPECTACULAR_SETTINGS = {
        "TITLE": "Main Server API",
        "DESCRIPTION": "Main Server for 'Octopus' app",
        "VERSION": "1.0.0",
        "SERVE_INCLUDE_SCHEMA": False,
    }
    TEMPLATES[0].update({"DIRS": [os.path.join(BASE_DIR, "templates/api_doc")]})
    STATICFILES_DIRS = (os.path.join(BASE_DIR, "api_doc/"),)
