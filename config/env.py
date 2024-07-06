from typing import Any


def env_to_list(env: str | None, default: list[str]) -> list[str]:
    return env.split(",") if env else default


def env_to_bool(env: str | None, default: Any) -> bool:
    return str(env).upper() in ["TRUE", "1", "YES"] if env else default
