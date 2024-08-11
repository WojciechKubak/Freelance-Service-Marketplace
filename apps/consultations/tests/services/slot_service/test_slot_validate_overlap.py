from apps.consultations.tests.factories import SlotFactory
from apps.consultations.services import SlotService
from django.core.exceptions import ValidationError
import pytest


class TestSlotValidateOverlap:

    @pytest.mark.django_db
    def test_slot_validate_overlap_without_excluding_existing_slot(self) -> None:
        slot = SlotFactory()
        slot_service = SlotService(consultation=slot.consultation)

        with pytest.raises(ValidationError) as e:
            slot_service._slot_validate_overlap(
                start_time=slot.start_time, end_time=slot.end_time
            )

        assert "['Slot overlaps with existing slots.']" == str(e.value)

    @pytest.mark.django_db
    def test_slot_validate_overlap_with_slot_id_excluded(self) -> None:
        slot = SlotFactory()
        slot_service = SlotService(consultation=slot.consultation)

        result = slot_service._slot_validate_overlap(
            start_time=slot.start_time, end_time=slot.end_time, slot_id=slot.id
        )

        assert None is result
