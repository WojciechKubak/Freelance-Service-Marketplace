from apps.consultations.tests.factories import ConsultationFactory
from apps.consultations.services import SlotService
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import pytest


@pytest.mark.django_db
def test_slot_validate_duration() -> None:
    consultation = ConsultationFactory()
    slot_service = SlotService(consultation=consultation)

    start_time = timezone.now()
    end_time = start_time + SlotService.MINIMUM_SLOT_DURATION - timedelta(minutes=1)

    with pytest.raises(ValidationError) as e:
        slot_service._slot_validate_duration(start_time=start_time, end_time=end_time)

    assert "['Slot duration must be at least 1 hour.']" == str(e.value)
