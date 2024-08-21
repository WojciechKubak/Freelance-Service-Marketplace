from apps.consultations.tests.factories import ConsultationFactory
from apps.consultations.services.consultations import consultation_change_visibility
from apps.consultations.models import Consultation
import pytest


@pytest.mark.django_db
def test_consultation_change_visibility() -> None:
    consultation = ConsultationFactory(is_visible=False)

    result = consultation_change_visibility(consultation, is_visible=True)
    expected = Consultation.objects.filter(is_visible=True).first()

    assert expected == result
    assert result.is_visible is True

    result = consultation_change_visibility(consultation, is_visible=False)
    expected = Consultation.objects.filter(is_visible=False).first()

    assert expected == result
    assert result.is_visible is False
