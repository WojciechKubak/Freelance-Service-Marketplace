from apps.consultations.tests.factories import ConsultationFactory, SlotFactory
from apps.consultations.services.slots import (
    SLOT_VALIDATE_OVERLAP,
    SLOT_VALIDATE_CONSULTATION_VISIBILITY,
    SLOT_VALIDATE_MINIMAL_DURATION_TIME,
    SlotService,
)
from django.core.exceptions import ValidationError
from django.utils import timezone
import pytest


class TestSlotCreate:

    def test_slot_create_raises_duration_error(self) -> None:
        consultation = ConsultationFactory()
        slot_service = SlotService(consultation=consultation)

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
            slot_service.slot_create(start_time=start_time, end_time=end_time)

    def test_slot_create_raises_overlap_error(self) -> None:
        consultation = ConsultationFactory()
        slot = SlotFactory(consultation=consultation)

        slot_service = SlotService(consultation=consultation)

        with pytest.raises(ValidationError, match=SLOT_VALIDATE_OVERLAP):
            slot_service.slot_create(start_time=slot.start_time, end_time=slot.end_time)

    def test_slot_create_raises_visibility_error(self) -> None:
        consultation = ConsultationFactory(is_visible=False)
        slot_service = SlotService(consultation=consultation)

        with pytest.raises(
            ValidationError, match=SLOT_VALIDATE_CONSULTATION_VISIBILITY
        ):
            slot_service._slot_validate_visibility()

    def test_slot_create_creates_db_instance_and_returns_it(self) -> None:
        consultation = ConsultationFactory(is_visible=True)
        slot_service = SlotService(consultation=consultation)

        start_time = timezone.now()
        end_time = start_time + timezone.timedelta(
            SlotService.SLOT_MINIMAL_DURATION_TIME_MINUTES
        )

        result = slot_service.slot_create(start_time=start_time, end_time=end_time)

        assert result == consultation.slots.first()
