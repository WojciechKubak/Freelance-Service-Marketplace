from apps.consultations.models import Consultation
from apps.consultations.utils import file_name_generate, text_to_file_local_upload
from apps.integrations.aws.client import text_to_file_upload
from apps.storages.enums import StorageType
from apps.categorization.models import Tag
from apps.users.models import User
from django.core.exceptions import ValidationError
from django.conf import settings


def consultation_create(
    user: User,
    title: str,
    content: str,
    price: float,
    tags: list[int],
) -> Consultation:
    existing_tags = Tag.objects.filter(id__in=tags)
    if existing_tags.count() != len(tags):
        raise ValidationError("One or more tags do not exist.")

    file_name = file_name_generate()

    if settings.STORAGE_TYPE_STRATEGY == StorageType.S3:
        text_to_file_upload(file_name=file_name, content=content)
    else:
        text_to_file_local_upload(file_name=file_name, content=content)

    consultation = Consultation(
        title=title, price=price, created_by=user, content_path=file_name
    )
    consultation.full_clean()
    consultation.save()
    consultation.tags.add(*existing_tags)

    return consultation


def consultation_update(
    consultation: Consultation,
    title: str | None = None,
    content: str | None = None,
    price: float | None = None,
    tags: list[int] | None = None,
) -> Consultation:

    if tags:
        existing_tags = Tag.objects.filter(id__in=tags)
        if existing_tags.count() != len(tags):
            raise ValidationError("One or more tags do not exist.")

        consultation.tags.clear()
        consultation.tags.add(*existing_tags)

    if content:
        if settings.STORAGE_TYPE_STRATEGY == StorageType.S3:
            text_to_file_upload(file_name=consultation.content_path, content=content)
        else:
            text_to_file_local_upload(
                file_name=consultation.content_path, content=content
            )

    consultation.title = title if title else consultation.title
    consultation.price = price if price else consultation.price

    consultation.full_clean()
    consultation.save()

    return consultation


def consultation_change_visibility(
    consultation: Consultation, is_visible: bool = False
) -> Consultation:
    # todo: this will also affect slots and bookings in some way
    consultation.is_visible = is_visible
    consultation.save()

    return consultation
