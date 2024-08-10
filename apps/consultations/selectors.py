from apps.consultations.models import Consultation
from apps.consultations.filters import ConsultationFilter
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from dataclasses import dataclass


@dataclass
class ConsultationSelectors:

    @staticmethod
    def consultation_list(
        *, filters: dict[str, str | int | float] = None
    ) -> QuerySet[Consultation]:
        filters = filters or {}
        queryset = Consultation.objects.filter(is_visible=True)

        return ConsultationFilter(filters, queryset).qs

    @staticmethod
    def consultation_detail(*, consultation_id: int) -> Consultation:
        return get_object_or_404(Consultation, id=consultation_id, is_visible=True)
