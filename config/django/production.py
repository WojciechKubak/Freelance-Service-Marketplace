from config.env import env_to_list, env_to_bool  # noqa
from .base import *  # noqa
import os


SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

ALLOWED_HOSTS = env_to_list(os.environ.get("DJANGO_ALLOWED_HOSTS"), [])

CORS_ALLOW_ALL_ORIGINS = False
CORS_ORIGIN_WHITELIST = env_to_list(os.environ.get("DJANGO_CORS_ORIGIN_WHITELIST"), [])

# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# SECURE_SSL_REDIRECT = env_to_bool(os.environ.get("DJANGO_SECURE_SSL_REDIRECT"), True)
# SECURE_CONTENT_TYPE_NOSNIFF = os.environ.get("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", True)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "db"),
        "USER": os.environ.get("POSTGRES_USER", "user"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "password1234"),
        "HOST": os.environ.get("POSTGRES_HOST", "postgres"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}
