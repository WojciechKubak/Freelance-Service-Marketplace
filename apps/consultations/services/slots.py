from apps.consultations.models import Consultation, Slot, Booking
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import datetime, timedelta
from typing import ClassVar
from dataclasses import dataclass


@dataclass
class SlotService:
    # todo: set this to hour unit also might export?
    MINIMUM_MEETING_DURATION: ClassVar[timedelta] = timedelta(hours=1)
    consultation: Consultation

    @staticmethod
    def meeting_validate_duration(*, start_time: datetime, end_time: datetime) -> None:
        if end_time - start_time < SlotService.MINIMUM_MEETING_DURATION:
            raise ValidationError("Meeting duration must be at least 1 hour.")

    def slot_create(self, *, start_time: datetime, end_time: datetime) -> Slot:
        self._slot_validate_visibility()
        self.meeting_validate_duration(start_time=start_time, end_time=end_time)
        self._slot_validate_overlap(start_time=start_time, end_time=end_time)

        slot = Slot(
            consultation=self.consultation, start_time=start_time, end_time=end_time
        )
        slot.full_clean()
        slot.save()

        return slot

    def slot_update(
        self,
        *,
        slot: Slot,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> Slot:
        # todo: we might move this to __post_init__
        self._slot_validate_visibility()

        slot.start_time = start_time if start_time else slot.start_time
        slot.end_time = end_time if end_time else slot.end_time

        self.meeting_validate_duration(
            start_time=slot.start_time, end_time=slot.end_time
        )
        self._slot_validate_overlap(
            start_time=slot.start_time, end_time=slot.end_time, slot_id=slot.id
        )

        slot.full_clean()
        slot.save()

        return slot

    def slot_delete(self, *, slot: Slot) -> None:
        bookings = slot.bookings.all()
        if bookings.exists():
            bookings.update(status=Booking.Status.CANCELLED)
            slot.is_cancelled = True
            slot.save()
        else:
            slot.delete()

    # todo: move error messages to constants
    def _slot_validate_visibility(self) -> None:
        if not self.consultation.is_visible:
            raise ValidationError("Consultation is not visible.")

    def _slot_validate_overlap(
        self, *, start_time: datetime, end_time: datetime, slot_id: int | None = None
    ) -> None:
        start_time_overlap = Q(start_time__lt=end_time, start_time__gte=start_time)
        end_time_overlap = Q(end_time__gt=start_time, end_time__lte=end_time)
        overlap_query = self.consultation.slots.filter(
            start_time_overlap | end_time_overlap
        )

        if slot_id:
            overlap_query = overlap_query.exclude(id=slot_id)

        if overlap_query.exists():
            raise ValidationError("Slot overlaps with existing slots.")
