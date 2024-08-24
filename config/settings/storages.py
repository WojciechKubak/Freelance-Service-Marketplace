from config.env import BASE_DIR, env_to_enum
from apps.storages.enums import StorageType
import os


STORAGE_TYPE_STRATEGY = env_to_enum(
    StorageType, os.getenv("STORAGE_TYPE", StorageType.LOCAL.value)
)

if STORAGE_TYPE_STRATEGY == StorageType.LOCAL:
    MEDIA_ROOT_NAME: str = "media"
    MEDIA_ROOT: str = os.path.join(BASE_DIR, MEDIA_ROOT_NAME)
    MEDIA_URL: str = f"/{MEDIA_ROOT_NAME}/"


if STORAGE_TYPE_STRATEGY == StorageType.S3:
    AWS_S3_ACCESS_KEY_ID: str = os.getenv("AWS_S3_ACCESS_KEY_ID")
    AWS_S3_SECRET_ACCESS_KEY: str = os.getenv("AWS_S3_SECRET_ACCESS_KEY")
    AWS_S3_BUCKET_NAME: str = os.getenv("AWS_S3_BUCKET_NAME")
