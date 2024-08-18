from config.env import BASE_DIR, env_to_enum
from apps.storages.enums import StorageType
from typing import Final
import os


STORAGE_TYPE_STRATEGY = env_to_enum(
    StorageType, os.getenv("STORAGE_TYPE", StorageType.LOCAL.value)
)

if STORAGE_TYPE_STRATEGY == StorageType.LOCAL:
    MEDIA_ROOT_NAME: Final[str] = "media"
    MEDIA_ROOT: Final[str] = os.path.join(BASE_DIR, MEDIA_ROOT_NAME)
    MEDIA_URL: Final[str] = f"/{MEDIA_ROOT_NAME}/"


if STORAGE_TYPE_STRATEGY == StorageType.S3:
    AWS_S3_ACCESS_KEY_ID: Final[str] = os.getenv("AWS_S3_ACCESS_KEY_ID")
    AWS_S3_SECRET_ACCESS_KEY: Final[str] = os.getenv("AWS_S3_SECRET_ACCESS_KEY")
    AWS_S3_BUCKET_NAME: Final[str] = os.getenv("AWS_S3_BUCKET_NAME")
