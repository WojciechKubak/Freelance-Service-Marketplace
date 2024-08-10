from apps.consultations.tests.factories import ConsultationFactory
from apps.consultations.services import SlotService
from django.core.exceptions import ValidationError
from django.utils import timezone
import pytest


@pytest.mark.django_db
def test_slot_validate_overlap() -> None:
    consultation = ConsultationFactory()
    slot_service = SlotService(consultation=consultation)

    start_time = timezone.now()
    end_time = start_time + SlotService.MINIMUM_SLOT_DURATION

    slot_service.slot_create(start_time=start_time, end_time=end_time)

    with pytest.raises(ValidationError) as e:
        slot_service.slot_create(start_time=start_time, end_time=end_time)

    assert "['Slot overlaps with existing slots.']" == str(e.value)
