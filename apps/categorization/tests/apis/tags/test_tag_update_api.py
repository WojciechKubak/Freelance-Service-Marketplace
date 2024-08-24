from apps.categorization.tests.factories import TagFactory, CategoryFactory
from apps.users.tests.factories import UserFactory, User
from apps.categorization.apis.tags import TagUpdateApi
from rest_framework.test import APIRequestFactory
from collections import OrderedDict
from typing import Callable, Any


class TestTagUpdateApi:

    def test_api_response_on_unauthorized_user(self) -> None:
        tag = TagFactory()

        factory = APIRequestFactory()
        request = factory.put(
            f"api/categorization/tags/{tag.id}/update",
            {"name": "Tag 1", "category_id": tag.category.id},
        )

        response = TagUpdateApi.as_view()(request, tag.id)

        expected_response_data = {
            "detail": "Authentication credentials were not provided."
        }

        assert 401 == response.status_code
        assert expected_response_data == response.data

    def test_api_response_on_invalid_tag_id(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        user = UserFactory(is_active=True)

        request = auth_request(
            user,
            "PUT",
            "api/categorization/tags/999/update",
            {"name": "Tag 1", "category_id": 1},
        )

        response = TagUpdateApi.as_view()(request, 999)

        expected_response_data = {"detail": "Not found."}

        assert 404 == response.status_code
        assert expected_response_data == response.data

    def test_api_response_for_user_that_is_not_instance_creator(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        tag = TagFactory()
        user = UserFactory(is_active=True)

        request = auth_request(
            user,
            "PUT",
            f"api/categorization/tags/{tag.id}/update",
            {"name": "Tag 1", "category_id": 1},
        )

        response = TagUpdateApi.as_view()(request, tag.id)

        expected_response_data = {
            "detail": "You do not have permission to perform this action."
        }

        assert 403 == response.status_code
        assert expected_response_data == response.data

    def test_api_response_on_successful_simple_fields_update(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        user = UserFactory(is_active=True)
        tag = TagFactory(created_by=user)

        request = auth_request(
            user,
            "PUT",
            f"api/categorization/tags/{tag.id}/update",
            {"name": "Tag 1", "category_id": tag.category.id},
        )

        response = TagUpdateApi.as_view()(request, tag.id)

        expected_response_data = OrderedDict(
            {
                "id": tag.id,
                "name": "Tag 1",
                "category": OrderedDict(
                    {
                        "id": tag.category.id,
                        "name": tag.category.name,
                    }
                ),
            }
        )

        assert 200 == response.status_code
        assert expected_response_data == response.data

    def test_api_response_on_successful_foreign_key_field_update(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        user = UserFactory(is_active=True)
        tag = TagFactory(created_by=user)
        category = CategoryFactory()

        request = auth_request(
            user,
            "PUT",
            f"api/categorization/tags/{tag.id}/update",
            {"category_id": category.id},
        )

        response = TagUpdateApi.as_view()(request, tag.id)

        expected_response_data = OrderedDict(
            {
                "id": tag.id,
                "name": tag.name,
                "category": OrderedDict(
                    {
                        "id": category.id,
                        "name": category.name,
                    }
                ),
            }
        )

        assert 200 == response.status_code
        assert expected_response_data == response.data
