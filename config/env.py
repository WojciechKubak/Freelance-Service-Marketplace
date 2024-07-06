from dotenv import load_dotenv

load_dotenv()


def env_to_list(env: str | None) -> list[str]:
    return env.split(",") if env else []


def env_to_bool(env: str | None) -> bool:
    return str(env).upper() in ["TRUE", "1", "YES"] if env else False
