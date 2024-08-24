from apps.consultations.models import Slot
from apps.consultations.filters import SlotFilter
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from datetime import datetime


def slot_list(*, filters: dict[str, int | datetime] = None) -> QuerySet[Slot]:
    filters = filters or {}
    queryset = Slot.objects.filter(is_cancelled=False, consultation__is_visible=True)

    return SlotFilter(filters, queryset).qs


def slot_detail(*, slot_id: int) -> Slot:
    return get_object_or_404(
        Slot, id=slot_id, is_cancelled=False, consultation__is_visible=True
    )
