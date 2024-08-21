from apps.consultations.tests.factories import ConsultationFactory
from apps.consultations.services import SlotService
from django.core.exceptions import ValidationError
from django.utils import timezone
import pytest


@pytest.mark.django_db
def test_slot_validate_duration() -> None:
    consultation = ConsultationFactory()
    slot_service = SlotService(consultation=consultation)

    start_time = timezone.now()
    end_time = (
        start_time
        + SlotService.MINIMUM_MEETING_DURATION
        - timezone.timedelta(minutes=1)
    )

    with pytest.raises(ValidationError) as e:
        slot_service.meeting_validate_duration(start_time=start_time, end_time=end_time)

    assert "['Meeting duration must be at least 1 hour.']" == str(e.value)
