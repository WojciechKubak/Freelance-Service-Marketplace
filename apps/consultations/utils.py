from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from datetime import datetime, timedelta
import uuid


def is_minimal_duration_time_valid(
    *, start_time: datetime, end_time: datetime, minimal_duration_time: int
) -> bool:
    minimal_duration = timedelta(minutes=minimal_duration_time)
    return end_time - start_time >= minimal_duration


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
