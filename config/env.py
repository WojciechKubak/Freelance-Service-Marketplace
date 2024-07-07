from pathlib import Path
from typing import Any


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def env_to_list(env: str | None, default: list[str]) -> list[str]:
    return env.split(",") if env else default


def env_to_bool(env: str | None, default: Any) -> bool:
    return str(env).upper() in ["TRUE", "1", "YES"] if env else default
