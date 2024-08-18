from apps.categorization.tests.factories import TagFactory
from apps.consultations.tests.factories import ConsultationFactory, Consultation
from apps.consultations.services import ConsultationService
from django.core.exceptions import ValidationError
from decimal import Decimal
import pytest


class TestConsultationUpdate:
    simple_field_data: dict[str, str | float] = {
        "title": "new_title",
        "content": "new_content",
        "price": Decimal("999.0"),
    }

    @pytest.mark.django_db
    def test_method_fails_due_to_non_existing_tags_id_and_raises_validation_error(
        self,
    ) -> None:
        consultation = ConsultationFactory()
        with pytest.raises(ValidationError):
            ConsultationService.consultation_update(
                consultation=consultation, **self.simple_field_data, tags=[999]
            )

    @pytest.mark.django_db
    def test_method_updates_instance_m2m_tag_field_and_returns_it(self) -> None:
        consultation = ConsultationFactory()
        tag = TagFactory()
        updated_tags = [tag.id]

        result = ConsultationService.consultation_update(
            consultation=consultation, tags=updated_tags
        )

        assert Consultation.objects.first() == result
        assert updated_tags == list(result.tags.values_list("id", flat=True))

    @pytest.mark.django_db
    def test_method_updates_instance_simple_fields_and_returns_it(self) -> None:
        consultation = ConsultationFactory()

        result = ConsultationService.consultation_update(
            consultation=consultation, **self.simple_field_data
        )

        assert Consultation.objects.first() == result
