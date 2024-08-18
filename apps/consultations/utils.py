from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import uuid


def _get_local_file_path(file_name: str, extension: str = ".txt") -> str:
    return f"{settings.MEDIA_ROOT}/{file_name}{extension}"


def file_name_generate() -> str:
    unique_id = uuid.uuid4()
    hex_filename = unique_id.hex

    return hex_filename


def text_to_file_local_upload(
    *, file_name: str, content: str, extension: str = ".txt"
) -> None:
    file_path = _get_local_file_path(file_name, extension)
    default_storage.save(file_path, ContentFile(content))


def local_file_get_content(*, file_name: str) -> str:
    file_path = _get_local_file_path(file_name)

    with default_storage.open(file_path) as file:
        return file.read().decode("utf-8")
