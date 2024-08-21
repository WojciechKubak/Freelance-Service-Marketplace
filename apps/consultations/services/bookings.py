from apps.consultations.models import Slot, Booking
from apps.consultations.services.slots import SlotService
from apps.integrations.zoom.client import create_meeting
from apps.users.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import datetime
from dataclasses import dataclass


@dataclass
class BookingService:
    slot: Slot

    def booking_create(
        self, *, user: User, start_time: datetime, end_time: datetime
    ) -> Booking:
        if self.slot.consultation.created_by == user:
            raise ValidationError("Cannot book own slot.")

        SlotService.meeting_validate_duration(start_time=start_time, end_time=end_time)
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
            raise ValidationError("Booking time must be within the slot time range.")

    def _booking_validate_overlap(
        self, *, start_time: datetime, end_time: datetime
    ) -> None:
        # todo: might merge with _slot_validate_overlap
        start_time_overlap = Q(start_time__lt=end_time, start_time__gte=start_time)
        end_time_overlap = Q(end_time__gt=start_time, end_time__lte=end_time)
        overlap_query = self.slot.bookings.filter(start_time_overlap | end_time_overlap)

        if overlap_query.exists():
            raise ValidationError("Booking overlaps with existing bookings.")
