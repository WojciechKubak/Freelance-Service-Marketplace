from apps.consultations.models import Consultation, Slot
from apps.consultations.filters import ConsultationFilter, SlotFilter
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from datetime import datetime
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


@dataclass
class SlotSelectors:

    @staticmethod
    def slot_list(*, filters: dict[str, int | datetime] = None) -> QuerySet[Slot]:
        filters = filters or {}
        queryset = Slot.objects.filter(
            is_cancelled=False, consultation__is_visible=True
        )

        return SlotFilter(filters, queryset).qs

    @staticmethod
    def slot_detail(*, slot_id: int) -> Slot:
        return get_object_or_404(
            Slot, id=slot_id, is_cancelled=False, consultation__is_visible=True
        )
