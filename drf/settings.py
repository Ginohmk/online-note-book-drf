from pathlib import Path


import os
from dotenv import load_dotenv

load_dotenv()

from corsheaders.defaults import default_methods, default_headers

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "Enter yours")
JWT_KEY = os.environ.get("JWT_KEY", "Enter yours")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "0.0.0.0",
    "localhost",
    "127.0.0.1",
    "44.241.249.189",
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third parties
    "corsheaders",
    "drf_spectacular",
    "rest_framework",
    # Apps
    "users",
    "note",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "drf.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "drf.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


# To get domain link
if os.environ.get("SSH_CLIENT", None) != None:
    DOMAIN_LINK = "44.241.249.189:8000"
else:
    DOMAIN_LINK = "127.0.0.1/8000"


if os.environ.get("SSH_CLIENT", None) != None:
    # Production DB
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "USER": os.environ.get("DB_USERNAME"),
            "NAME": os.environ.get("DB_NAME"),
            "PASSWORD": os.environ.get("DB_PASSWORD"),
            "HOST": os.environ.get("DB_HOSTNAME"),
            "PORT": "3306",
        }
    }

else:
    # Local DB
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": "online_note",
            "USER": "kanu",
            "PASSWORD": "password",
            "HOST": "localhost",
            "PORT": "3306",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


STATIC_URL = "/static/"
STATIC_ROOT = "static"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# For spectacualer Swagger
REST_FRAMEWORK = {
    # YOUR SETTINGS
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Online Note",
    "DESCRIPTION": "Online Note taker for Tunga company",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # OTHER SETTINGS
}


# Specify Where user model is loacated

AUTH_USER_MODEL = "users.User"

#  Cors setup
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://0.0.0.0:8000",
    "http://44.241.249.189:8000",
]
CORS_ALLOW_METHODS = (*default_methods,)
CORS_ALLOW_HEADERS = (*default_headers,)


# Email Setup
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get("HOST_EMAIL_USER", "Enter yours")
EMAIL_HOST_PASSWORD = os.environ.get("HOST_EMAIL_PASSWORD", "Enter yours")


# Celery settings
CELERY_BROKER_URL = "redis://127.0.0.1:6379"
# broker_connection_retry_on_startup = True

# schedule task
CELERY_BEAT_SCHEDULE = {
    "reminder_func": {"task": "note.tasks.due_date_reminder", "schedule": 20}
}
