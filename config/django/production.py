from config.env import env_to_list
from .base import *  # noqa
import os


SECRET_KEY = os.environ["SECRET_KEY"]

ALLOWED_HOSTS = env_to_list(os.environ.get("DJANGO_ALLOWED_HOSTS"), [])
