from apps.consultations.tests.factories import SlotFactory
from apps.consultations.services import BookingService
from django.core.exceptions import ValidationError
from django.utils import timezone
import pytest


@pytest.mark.django_db
def test_booking_validate_in_slot_range() -> None:
    slot = SlotFactory()
    booking_service = BookingService(slot=slot)

    start_time = slot.start_time
    end_time = slot.start_time + timezone.timedelta(minutes=15)

    booking_service._booking_validate_in_slot_range(
        start_time=start_time, end_time=end_time
    )

    start_time = slot.start_time - timezone.timedelta(minutes=15)
    end_time = slot.end_time

    with pytest.raises(ValidationError) as e:
        booking_service._booking_validate_in_slot_range(
            start_time=start_time, end_time=end_time
        )

    assert "Booking time must be within the slot time range." in str(e.value)
