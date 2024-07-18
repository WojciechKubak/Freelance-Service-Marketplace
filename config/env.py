from django.core.exceptions import ImproperlyConfigured
from pathlib import Path
from enum import Enum
import os


BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = os.path.join(BASE_DIR, "apps")


def env_to_list(env: str | None, default: list[str]) -> list[str]:
    return env.split(",") if env else default


def env_to_bool(env: str | None, default: bool) -> bool:
    return str(env).upper() in ["TRUE", "1", "YES"] if env else default


def env_to_enum(enum_class: type[Enum], env: str | None) -> Enum | None:
    for choice in enum_class:
        if choice.value.lower() == env.lower():
            return choice

    raise ImproperlyConfigured(f"Invalid value for {enum_class.__name__}: {env}")
