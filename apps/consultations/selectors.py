from apps.consultations.models import Consultation
from apps.consultations.filters import ConsultationFilter
from django.db.models import QuerySet
from dataclasses import dataclass
from typing import Any


@dataclass
class ConsultationSelectors:

    @staticmethod
    def consultation_list(*, filters: dict[str, Any] = None) -> QuerySet:
        filters = filters or {}
        queryset = Consultation.objects.filter(is_visible=True)

        return ConsultationFilter(filters, queryset).qs
