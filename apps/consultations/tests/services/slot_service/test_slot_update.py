from apps.consultations.tests.factories import ConsultationFactory, SlotFactory
from apps.consultations.services import SlotService
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import pytest


class TestSlotUpdate:

    @pytest.mark.django_db
    def test_slot_update_raises_duration_error(self) -> None:
        slot = SlotFactory()
        slot_service = SlotService(consultation=slot.consultation)

        start_time = timezone.now()
        end_time = (
            start_time + SlotService.MINIMUM_MEETING_DURATION - timedelta(minutes=1)
        )

        with pytest.raises(ValidationError) as e:
            slot_service.slot_update(
                slot=slot, start_time=start_time, end_time=end_time
            )

        assert "['Meeting duration must be at least 1 hour.']" == str(e.value)

    @pytest.mark.django_db
    def test_slot_update_raises_overlap_error(self) -> None:
        consultation = ConsultationFactory()
        slot1, slot2 = SlotFactory.create_batch(2, consultation=consultation)
        slot_service = SlotService(consultation=consultation)

        with pytest.raises(ValidationError) as e:
            slot_service.slot_update(
                slot=slot1, start_time=slot2.start_time, end_time=slot2.end_time
            )

        assert "['Slot overlaps with existing slots.']" == str(e.value)

    @pytest.mark.django_db
    def test_slot_update_raises_visibility_error(self) -> None:
        consultation = ConsultationFactory(is_visible=False)
        SlotFactory(consultation=consultation)

        slot_service = SlotService(consultation)

        with pytest.raises(ValidationError) as e:
            slot_service.slot_update(
                slot=slot_service.consultation.slots.first(),
                start_time=timezone.now(),
                end_time=timezone.now() + SlotService.MINIMUM_MEETING_DURATION,
            )

        assert "['Consultation is not visible.']" == str(e.value)

    @pytest.mark.django_db
    def test_slot_update_modifies_db_instance_and_returns_it(self) -> None:
        slot = SlotFactory()
        slot_service = SlotService(consultation=slot.consultation)

        new_start_time = timezone.now()
        new_end_time = new_start_time + SlotService.MINIMUM_MEETING_DURATION

        result = slot_service.slot_update(
            slot=slot, start_time=new_start_time, end_time=new_end_time
        )

        assert slot == result
        assert new_start_time == result.start_time
        assert new_end_time == result.end_time
