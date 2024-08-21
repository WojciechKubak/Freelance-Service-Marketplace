from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from typing import Any


# https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/common/utils.py
def assert_settings(
    required: list[str], error_prefix: str | None = None
) -> dict[str, Any]:
    present: dict[str, Any] = {}
    missing: list[str] = []

    for setting in required:
        if hasattr(settings, setting):
            present[setting] = getattr(settings, setting)
        else:
            missing.append(setting)

    if missing:
        prefix = f"{error_prefix}: " if error_prefix else ""
        raise ImproperlyConfigured(f"{prefix} missing settings: {', '.join(missing)}")

    return present
