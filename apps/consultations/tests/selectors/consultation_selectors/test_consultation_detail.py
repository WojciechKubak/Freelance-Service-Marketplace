from apps.consultations.tests.factories import ConsultationFactory
from apps.consultations.selectors import ConsultationSelectors
from django.http import Http404
import pytest


class TestConsultationDetail:

    @pytest.mark.django_db
    def test_consultation_detail_raises_404(self) -> None:
        consultation = ConsultationFactory(is_visible=False)
        with pytest.raises(Http404):
            ConsultationSelectors.consultation_detail(consultation_id=consultation.id)

    @pytest.mark.django_db
    def test_consultation_detail_returns_consultation_obj(self) -> None:
        consultation = ConsultationFactory(is_visible=True)
        result = ConsultationSelectors.consultation_detail(
            consultation_id=consultation.id
        )
        assert consultation == result
