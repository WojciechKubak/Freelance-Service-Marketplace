from apps.consultations.tests.factories import BookingFactory
from apps.consultations.services.bookings import BookingService, SlotService
from django.core.exceptions import ValidationError
import pytest


@pytest.mark.django_db
def test_booking_validate_overlap() -> None:
    booking = BookingFactory()

    booking_service = BookingService(slot=booking.slot)

    booking_service._booking_validate_overlap(
        start_time=booking.end_time,
        end_time=booking.end_time + SlotService.MINIMUM_MEETING_DURATION,
    )

    with pytest.raises(ValidationError) as e:
        booking_service._booking_validate_overlap(
            start_time=booking.start_time, end_time=booking.end_time
        )

    assert "Booking overlaps with existing bookings." in str(e.value)
