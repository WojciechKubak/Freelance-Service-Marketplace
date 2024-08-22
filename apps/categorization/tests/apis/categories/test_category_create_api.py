from apps.categorization.tests.factories import UserFactory
from apps.categorization.apis.categories import CategoryCreateApi
from apps.users.models import User
from rest_framework.test import APIRequestFactory
from collections import OrderedDict
from typing import Callable, Any
import pytest


class TestCategoryCreateApi:
    simple_field_data: dict[str, Any] = {
        "name": "Category 1",
        "description": "Description 1",
    }

    @pytest.mark.django_db
    def test_api_response_on_unauthorized_user(self) -> None:
        factory = APIRequestFactory()
        request = factory.post("api/categories/create", self.simple_field_data)

        response = CategoryCreateApi.as_view()(request)

        expected_response_data = {
            "detail": "Authentication credentials were not provided."
        }

        assert 401 == response.status_code
        assert expected_response_data == response.data

    @pytest.mark.django_db
    def test_api_response_on_successfully_created_category(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:

        request = auth_request(
            UserFactory(is_active=True, is_admin=True),
            "POST",
            "/api/categories/create",
            self.simple_field_data,
        )

        response = CategoryCreateApi.as_view()(request)

        expected_response_data = OrderedDict({"id": 1, **self.simple_field_data})

        assert 201 == response.status_code
        assert expected_response_data == response.data
