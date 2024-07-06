"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

from config.django.base import DEBUG
from django.core.wsgi import get_wsgi_application
import os


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.django.base" if DEBUG else "config.django.production",
)

application = get_wsgi_application()
