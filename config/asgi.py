"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

from config.django.base import DEBUG
from django.core.asgi import get_asgi_application
import os


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.django.base" if DEBUG else "config.django.production",
)

application = get_asgi_application()
