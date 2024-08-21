from apps.consultations.models import Consultation, Slot, Booking
from apps.consultations.filters import ConsultationFilter, SlotFilter
from apps.consultations.utils import local_file_get_content
from apps.users.models import User
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from datetime import datetime
from typing import Any
from dataclasses import dataclass


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
        consultation = get_object_or_404(
            Consultation, id=consultation_id, is_visible=True
        )
        content = local_file_get_content(file_name=consultation.content_path)

        return consultation_with_content(consultation=consultation, content=content)


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


@dataclass
class BookingSelectors:

    @staticmethod
    def booking_list(*, user: User) -> QuerySet[Booking]:
        return Booking.objects.filter(booked_by=user)
