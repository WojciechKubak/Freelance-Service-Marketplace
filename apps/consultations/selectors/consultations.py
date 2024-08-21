from apps.consultations.models import Consultation
from apps.consultations.filters import ConsultationFilter
from apps.consultations.utils import local_file_get_content
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from typing import Any


def consultation_with_content(
    *, consultation: Consultation, content: str
) -> dict[str, Any]:
    return {
        "id": consultation.id,
        "title": consultation.title,
        "content": content,
        "price": consultation.price,
        "tags": consultation.tags,
    }


def consultation_list(
    *, filters: dict[str, str | int | float] = None
) -> QuerySet[Consultation]:
    filters = filters or {}
    queryset = Consultation.objects.filter(is_visible=True)

    return ConsultationFilter(filters, queryset).qs


def consultation_detail(*, consultation_id: int) -> Consultation:
    consultation = get_object_or_404(Consultation, id=consultation_id, is_visible=True)
    content = local_file_get_content(file_name=consultation.content_path)

    return consultation_with_content(consultation=consultation, content=content)
