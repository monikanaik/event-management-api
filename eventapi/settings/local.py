# settings/development.py
from datetime import timedelta

from .base import *

# SECRET_KEY = os.environ.get("SECRET_KEY")
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "fallback-secret-key")

DEBUG = True

ALLOWED_HOSTS = ["*"]

# Development-specific database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",  # or 'django.db.backends.mysql'
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),  # Default PostgreSQL port
        "TEST": {"NAME": "test"},
    },
}
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "SLIDING_TOKEN_LIFETIME": timedelta(days=30),
    "SLIDING_TOKEN_REFRESH_LIFETIME_LATE_USER": timedelta(days=1),
    "SLIDING_TOKEN_LIFETIME_LATE_USER": timedelta(days=30),
}

# Static and media files for development
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"

AUTH_USER_MODEL = "api.User"
