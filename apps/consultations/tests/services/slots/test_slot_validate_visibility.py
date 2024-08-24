from apps.consultations.tests.factories import ConsultationFactory
from apps.consultations.services.slots import (
    SlotService,
    SLOT_VALIDATE_CONSULTATION_VISIBILITY,
)
from django.core.exceptions import ValidationError
import pytest


@pytest.mark.django_db
def test_slot_validate_visibility() -> None:
    consultation = ConsultationFactory(is_visible=False)
    slot_service = SlotService(consultation=consultation)

    with pytest.raises(ValidationError, match=SLOT_VALIDATE_CONSULTATION_VISIBILITY):
        slot_service._slot_validate_visibility()
