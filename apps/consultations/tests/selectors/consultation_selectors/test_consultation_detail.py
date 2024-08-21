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
    def test_consultation_detail_returns_consultation_with_content(
        self, mock_local_file_get_content
    ) -> None:
        consultation = ConsultationFactory(is_visible=True)

        result = ConsultationSelectors.consultation_detail(
            consultation_id=consultation.id
        )

        expected_result = {
            "id": consultation.id,
            "title": consultation.title,
            "content": mock_local_file_get_content.return_value,
            "price": consultation.price,
            "tags": consultation.tags,
        }

        assert expected_result == result
