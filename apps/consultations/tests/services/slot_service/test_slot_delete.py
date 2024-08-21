from apps.consultations.tests.factories import SlotFactory, Booking, Slot
from apps.consultations.services import SlotService
import pytest


class TestSlotDelete:

    @pytest.mark.django_db
    def test_call_on_slot_with_bookings_sets_is_cancelled_flag_and_all_bookings_status(
        self,
    ) -> None:
        slot = SlotFactory(generate_bookings=True)

        slot_service = SlotService(consultation=slot.consultation)

        slot_service.slot_delete(slot=slot)

        assert slot.is_cancelled
        assert all(
            booking.status == Booking.Status.CANCELLED
            for booking in slot.bookings.all()
        )

    @pytest.mark.django_db
    def test_call_on_slot_without_bookings_deletes_instance(self) -> None:
        slot = SlotFactory(generate_bookings=False)
        slot_service = SlotService(consultation=slot.consultation)

        slot_service.slot_delete(slot=slot)

        assert not Slot.objects.filter(id=slot.id).exists()
