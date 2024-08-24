from apps.consultations.tests.factories import BookingFactory
from apps.consultations.services.bookings import (
    BOOKING_VALIDATE_OVERLAP,
    BookingService,
)
from django.utils import timezone
from django.core.exceptions import ValidationError
import pytest


@pytest.mark.django_db
def test_booking_validate_overlap() -> None:
    booking = BookingFactory()

    booking_service = BookingService(slot=booking.slot)

    booking_service._booking_validate_overlap(
        start_time=booking.end_time,
        end_time=booking.end_time
        + timezone.timedelta(BookingService.BOOKING_MINIMAL_DURATION_TIME_MINUTES),
    )

    with pytest.raises(ValidationError, match=BOOKING_VALIDATE_OVERLAP):
        booking_service._booking_validate_overlap(
            start_time=booking.start_time, end_time=booking.end_time
        )
