from apps.users.tests.factories import UserFactory
from apps.categorization.tests.factories import TagFactory
from apps.consultations.tests.factories import ConsultationFactory
from apps.consultations.services import ConsultationService
from apps.consultations.models import Consultation
from django.core.exceptions import ValidationError
import pytest


class TestConsultationCreate:
    simple_field_data: dict[str, str | float] = {
        "title": "Test consultation",
        "description": "Test description",
        "price": 100.0,
    }

    @pytest.mark.django_db
    def test_method_fails_due_to_single_consultation_for_user_constraint(
        self,
    ) -> None:
        consultation = ConsultationFactory()

        with pytest.raises(ValidationError):
            ConsultationService.consultation_create(
                user=consultation.created_by,
                **self.simple_field_data,
                tags=[TagFactory().id]
            )

    @pytest.mark.django_db
    def test_method_fails_due_to_non_existing_tags_id(self) -> None:
        with pytest.raises(ValidationError):
            ConsultationService.consultation_create(
                user=UserFactory(), **self.simple_field_data, tags=[999]
            )

    @pytest.mark.django_db
    def test_method_creates_instance_with_expected_data_and_returns_it(
        self,
    ) -> None:
        tags = [TagFactory().id, TagFactory().id]

        result = ConsultationService.consultation_create(
            user=UserFactory(), **self.simple_field_data, tags=tags
        )

        assert Consultation.objects.first() == result
        assert self.simple_field_data.items() <= result.__dict__.items()
        assert tags == list(result.tags.values_list("id", flat=True))
