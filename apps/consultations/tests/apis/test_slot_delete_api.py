from apps.consultations.tests.factories import SlotFactory
from apps.consultations.apis import SlotDeleteApi
from apps.users.models import User
from rest_framework.test import APIRequestFactory
from typing import Callable, Any
import pytest


class TestSlotDeleteApi:

    @pytest.mark.django_db
    def test_api_response_on_instance_not_found(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        slot = SlotFactory()
        request = auth_request(
            slot.consultation.created_by,
            "DELETE",
            "/api/consultations/slots/999/delete/",
        )

        response = SlotDeleteApi.as_view()(request, 999)

        assert 404 == response.status_code

    @pytest.mark.django_db
    def test_api_response_on_successful_delete(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        slot = SlotFactory()
        request = auth_request(
            slot.consultation.created_by,
            "DELETE",
            f"/api/consultations/slots/{slot.id}/delete/",
        )

        response = SlotDeleteApi.as_view()(request, slot.id)

        assert 204 == response.status_code
