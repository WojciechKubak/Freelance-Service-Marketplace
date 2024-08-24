from apps.consultations.models import Slot, Booking
from apps.consultations.utils import is_minimal_duration_time_valid
from apps.integrations.zoom.meetings import create_meeting
from apps.users.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import datetime
from dataclasses import dataclass
from typing import ClassVar


BOOKING_CANNOT_BOOK_OWN_SLOT: str = "Cannot book own slot."
BOOKING_VALIDATE_WITHING_SLOT_RANGE: str = (
    "Booking time must be within the slot time range."
)
BOOKING_VALIDATE_OVERLAP: str = "Booking overlaps with existing bookings."
BOOKING_VALIDATE_MINIMAL_DURATION_TIME: str = (
    "Meeting duration must be at least {} minutes."
)


@dataclass
class BookingService:
    BOOKING_MINIMAL_DURATION_TIME_MINUTES: ClassVar[int] = 60
    slot: Slot

    def booking_create(
        self, *, user: User, start_time: datetime, end_time: datetime
    ) -> Booking:
        if self.slot.consultation.created_by == user:
            raise ValidationError(BOOKING_CANNOT_BOOK_OWN_SLOT)
        if not is_minimal_duration_time_valid(
            start_time=start_time,
            end_time=end_time,
            minimal_duration_time=self.BOOKING_MINIMAL_DURATION_TIME_MINUTES,
        ):
            raise ValidationError(
                BOOKING_VALIDATE_MINIMAL_DURATION_TIME.format(
                    self.BOOKING_MINIMAL_DURATION_TIME_MINUTES
                )
            )
        self._booking_validate_in_slot_range(start_time=start_time, end_time=end_time)
        self._booking_validate_overlap(start_time=start_time, end_time=end_time)

        meeting_details = create_meeting(
            topic=self.slot.consultation.title,
            start_time=start_time,
            duration=(end_time - start_time).seconds // 60,
        )

        booking = Booking(
            slot=self.slot,
            booked_by=user,
            start_time=start_time,
            end_time=end_time,
            url=meeting_details.join_url,
        )
        booking.full_clean()
        booking.save()

        return booking

    def _booking_validate_in_slot_range(
        self, *, start_time: datetime, end_time: datetime
    ) -> None:
        if not (self.slot.start_time <= start_time < self.slot.end_time) or not (
            self.slot.start_time < end_time <= self.slot.end_time
        ):
            raise ValidationError(BOOKING_VALIDATE_WITHING_SLOT_RANGE)

    def _booking_validate_overlap(
        self, *, start_time: datetime, end_time: datetime
    ) -> None:
        # todo: might merge with _slot_validate_overlap
        start_time_overlap = Q(start_time__lt=end_time, start_time__gte=start_time)
        end_time_overlap = Q(end_time__gt=start_time, end_time__lte=end_time)
        overlap_query = self.slot.bookings.filter(start_time_overlap | end_time_overlap)

        if overlap_query.exists():
            raise ValidationError(BOOKING_VALIDATE_OVERLAP)
