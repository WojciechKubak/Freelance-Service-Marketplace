from config.env import env_to_list, env_to_bool
from .base import *  # noqa
import os


SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = env_to_list(os.environ.get("DJANGO_ALLOWED_HOSTS"), [])

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = env_to_bool(os.environ.get("SECURE_SSL_REDIRECT"), True)
# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = env_to_bool(
    os.environ.get("SECURE_CONTENT_TYPE_NOSNIFF"), True
)
