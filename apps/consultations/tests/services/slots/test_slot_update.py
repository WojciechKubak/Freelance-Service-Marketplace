from apps.consultations.tests.factories import ConsultationFactory, SlotFactory
from apps.consultations.services.slots import (
    SLOT_VALIDATE_CONSULTATION_VISIBILITY,
    SLOT_VALIDATE_MINIMAL_DURATION_TIME,
    SLOT_VALIDATE_OVERLAP,
    SlotService,
)
from django.core.exceptions import ValidationError
from django.utils import timezone
import pytest


class TestSlotUpdate:

    def test_slot_update_raises_duration_error(self) -> None:
        slot = SlotFactory()
        slot_service = SlotService(consultation=slot.consultation)

        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(
            minutes=SlotService.SLOT_MINIMAL_DURATION_TIME_MINUTES - 1
        )

        with pytest.raises(
            ValidationError,
            match=SLOT_VALIDATE_MINIMAL_DURATION_TIME.format(
                SlotService.SLOT_MINIMAL_DURATION_TIME_MINUTES
            ),
        ):
            slot_service.slot_update(
                slot=slot, start_time=start_time, end_time=end_time
            )

    def test_slot_update_raises_overlap_error(self) -> None:
        consultation = ConsultationFactory()
        slot1, slot2 = SlotFactory.create_batch(2, consultation=consultation)
        slot_service = SlotService(consultation=consultation)

        with pytest.raises(ValidationError, match=SLOT_VALIDATE_OVERLAP):
            slot_service.slot_update(
                slot=slot1, start_time=slot2.start_time, end_time=slot2.end_time
            )

    def test_slot_update_raises_visibility_error(self) -> None:
        consultation = ConsultationFactory(is_visible=False)
        SlotFactory(consultation=consultation)

        slot_service = SlotService(consultation)

        with pytest.raises(
            ValidationError, match=SLOT_VALIDATE_CONSULTATION_VISIBILITY
        ):
            slot_service.slot_update(
                slot=slot_service.consultation.slots.first(),
                start_time=timezone.now(),
                end_time=timezone.now()
                + timezone.timedelta(
                    minutes=SlotService.SLOT_MINIMAL_DURATION_TIME_MINUTES
                ),
            )

    def test_slot_update_modifies_db_instance_and_returns_it(self) -> None:
        slot = SlotFactory()
        slot_service = SlotService(consultation=slot.consultation)

        new_start_time = timezone.now()
        new_end_time = new_start_time + timezone.timedelta(
            minutes=SlotService.SLOT_MINIMAL_DURATION_TIME_MINUTES
        )

        result = slot_service.slot_update(
            slot=slot, start_time=new_start_time, end_time=new_end_time
        )

        assert slot == result
        assert new_start_time == result.start_time
        assert new_end_time == result.end_time
