from apps.consultations.tests.factories import ConsultationFactory
from apps.consultations.apis.consultation_api import ConsultationDetailApi
from rest_framework.test import APIRequestFactory
from collections import OrderedDict
import pytest


class TestConsultationDetailApi:
    factory: APIRequestFactory = APIRequestFactory()
    url: str = "/api/consultations/"

    @pytest.mark.django_db
    def test_api_response_on_failed_due_to_not_found_result(self) -> None:
        request = self.factory.get(f"{self.url}999/")
        response = ConsultationDetailApi.as_view()(request, consultation_id=1)

        assert 404 == response.status_code
        assert {"detail": "Not found."} == response.data

    @pytest.mark.django_db
    def test_api_response_on_success(self) -> None:
        consultation = ConsultationFactory()
        request = self.factory.get(f"{self.url}{consultation.id}/")

        response = ConsultationDetailApi.as_view()(
            request, consultation_id=consultation.id
        )

        expected_response_data = OrderedDict(
            {
                "id": consultation.id,
                "title": consultation.title,
                "description": consultation.description,
                "price": float(consultation.price),
                "tags": [
                    OrderedDict({"id": tag.id, "name": tag.name})
                    for tag in consultation.tags.all()
                ],
            }
        )

        assert 200 == response.status_code
        assert expected_response_data == response.data
