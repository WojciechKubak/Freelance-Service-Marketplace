from apps.categorization.tests.factories import UserFactory, CategoryFactory
from apps.categorization.apis.tags import TagCreateApi
from apps.users.models import User
from rest_framework.test import APIRequestFactory
from collections import OrderedDict
from typing import Callable, Any


class TestTagCreateApi:
    simple_field_data: dict[str, Any] = {"name": "Tag 1"}

    def test_api_response_on_unauthorized_user(self) -> None:
        factory = APIRequestFactory()
        request = factory.post("api/categories/tags/create", self.simple_field_data)

        response = TagCreateApi.as_view()(request)

        expected_response_data = {
            "detail": "Authentication credentials were not provided."
        }

        assert 401 == response.status_code
        assert expected_response_data == response.data

    def test_api_response_on_missing_required_field(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        request = auth_request(
            UserFactory(is_active=True, is_admin=True),
            "POST",
            "/api/categories/tags/create",
            self.simple_field_data,
        )

        response = TagCreateApi.as_view()(request)

        expected_response_data = {
            "detail": {"category_id": ["This field is required."]}
        }

        assert 400 == response.status_code
        assert expected_response_data == response.data

    def test_api_response_on_successfully_created_tag(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        category = CategoryFactory()

        request = auth_request(
            UserFactory(is_active=True, is_admin=True),
            "POST",
            "/api/categories/tags/create",
            {**self.simple_field_data, "category_id": category.id},
        )

        response = TagCreateApi.as_view()(request)

        expected_response_data = OrderedDict(
            {
                "id": 1,
                **self.simple_field_data,
                "category": OrderedDict({"id": category.id, "name": category.name}),
            }
        )

        assert 201 == response.status_code
        assert expected_response_data == response.data
