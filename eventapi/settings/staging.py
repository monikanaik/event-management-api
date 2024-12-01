# settings/production.py

from .base import *
import os

# SECRET_KEY = os.environ.get("SECRET_KEY")
SECRET_KEY = "django-insecure-jg5=-3ej&yie50s#5ga=n9-j5bg78_s*^byys85af1us@_c#3l"

DEBUG = False

ALLOWED_HOSTS = ["*"]

# Production-specific database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    },
}

# Static and media files for production
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
