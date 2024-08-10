from apps.consultations.apis import ConsultationListApi
from apps.consultations.tests.factories import ConsultationFactory
from rest_framework.test import APIRequestFactory
from collections import OrderedDict
import pytest


class TestConsultationListApi:
    factory: APIRequestFactory = APIRequestFactory()
    url: str = "/api/consultations/"

    @pytest.mark.django_db
    def test_api_response_returns_no_results_on_filter_provided(self) -> None:
        title = "Consultation 1"
        ConsultationFactory(title=title)
        request = self.factory.get(f"{self.url}?title=other_{title}")

        response = ConsultationListApi.as_view()(request)

        assert 200 == response.status_code
        assert [] == response.data

    @pytest.mark.django_db
    def test_api_response_returns_results_on_filter_provided(self) -> None:
        title = "Consultation 1"
        consultation = ConsultationFactory(title=title)
        request = self.factory.get(f"{self.url}?title={title}")

        response = ConsultationListApi.as_view()(request)

        expected_response_data = [
            OrderedDict(
                {
                    "id": consultation.id,
                    "title": "Consultation 1",
                    "price": float(consultation.price),
                    "tags": [
                        OrderedDict({"id": tag.id, "name": tag.name})
                        for tag in consultation.tags.all()
                    ],
                }
            )
        ]

        assert 200 == response.status_code
        assert expected_response_data == response.data
