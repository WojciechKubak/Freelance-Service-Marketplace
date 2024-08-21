from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid


def file_name_generate(extension: str = ".txt") -> str:
    unique_id = uuid.uuid4()
    hex_filename = unique_id.hex

    return f"{hex_filename}{extension}"


def text_to_file_local_upload(*, file_name: str, content: str) -> None:
    if default_storage.exists(file_name):
        default_storage.delete(file_name)

    default_storage.save(file_name, ContentFile(content))


def local_file_get_content(*, file_name: str) -> str:
    with default_storage.open(file_name) as file:
        return file.read().decode("utf-8")
