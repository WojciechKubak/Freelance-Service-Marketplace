from apps.consultations.tests.factories import ConsultationFactory, SlotFactory
from apps.consultations.services import SlotService
from django.core.exceptions import ValidationError
from django.utils import timezone
import pytest


class TestSlotCreate:

    @pytest.mark.django_db
    def test_slot_create_raises_duration_error(self) -> None:
        consultation = ConsultationFactory()
        slot_service = SlotService(consultation=consultation)

        start_time = timezone.now()
        end_time = (
            start_time
            + SlotService.MINIMUM_MEETING_DURATION
            - timezone.timedelta(minutes=1)
        )

        with pytest.raises(ValidationError) as e:
            slot_service.slot_create(start_time=start_time, end_time=end_time)

        assert "['Meeting duration must be at least 1 hour.']" == str(e.value)

    @pytest.mark.django_db
    def test_slot_create_raises_overlap_error(self) -> None:
        consultation = ConsultationFactory()
        slot = SlotFactory(consultation=consultation)

        slot_service = SlotService(consultation=consultation)

        with pytest.raises(ValidationError) as e:
            slot_service.slot_create(start_time=slot.start_time, end_time=slot.end_time)

        assert "['Slot overlaps with existing slots.']" == str(e.value)

    @pytest.mark.django_db
    def test_slot_create_raises_visibility_error(self) -> None:
        consultation = ConsultationFactory(is_visible=False)
        slot_service = SlotService(consultation=consultation)

        with pytest.raises(ValidationError) as e:
            slot_service._slot_validate_visibility()

        assert "['Consultation is not visible.']" == str(e.value)

    @pytest.mark.django_db
    def test_slot_create_creates_db_instance_and_returns_it(self) -> None:
        consultation = ConsultationFactory(is_visible=True)
        slot_service = SlotService(consultation=consultation)

        start_time = timezone.now()
        end_time = start_time + SlotService.MINIMUM_MEETING_DURATION

        result = slot_service.slot_create(start_time=start_time, end_time=end_time)

        assert result == consultation.slots.first()
