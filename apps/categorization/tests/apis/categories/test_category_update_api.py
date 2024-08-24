from apps.categorization.tests.factories import CategoryFactory
from apps.users.tests.factories import UserFactory, User
from apps.categorization.apis.categories import CategoryUpdateApi
from rest_framework.test import APIRequestFactory
from collections import OrderedDict
from typing import Callable, Any


class TestCategoryUpdateApi:
    simple_field_data: dict[str, str] = {
        "name": "Category 1",
        "description": "Description 1",
    }

    def test_api_response_on_unauthorized_user(self) -> None:
        category = CategoryFactory()

        factory = APIRequestFactory()
        request = factory.put(
            f"api/categorization/categories/{category.id}/update",
            self.simple_field_data,
        )

        response = CategoryUpdateApi.as_view()(request, category.id)

        expected_response_data = {
            "detail": "Authentication credentials were not provided."
        }

        assert 401 == response.status_code
        assert expected_response_data == response.data

    def test_api_response_on_invalid_category_id(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        user = UserFactory(is_active=True)

        request = auth_request(
            user,
            "PUT",
            "api/categorization/categories/999/update",
            self.simple_field_data,
        )

        response = CategoryUpdateApi.as_view()(request, 999)

        expected_response_data = {"detail": "Not found."}

        assert 404 == response.status_code
        assert expected_response_data == response.data

    def test_api_response_for_user_that_is_not_instance_creator(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        first, second = UserFactory.create_batch(2, is_active=True)
        category = CategoryFactory(created_by=first)

        request = auth_request(
            second,
            "PUT",
            f"api/categorization/categories/{category.id}/update",
            self.simple_field_data,
        )

        response = CategoryUpdateApi.as_view()(request, category.id)

        expected_response_data = {
            "detail": "You do not have permission to perform this action."
        }

        assert 403 == response.status_code
        assert expected_response_data == response.data

    def test_api_response_on_missing_all_data_fields(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        user = UserFactory(is_active=True)
        category = CategoryFactory(created_by=user)

        request = auth_request(
            user, "PUT", f"api/categorization/categories/{category.id}/update", {}
        )

        response = CategoryUpdateApi.as_view()(request, category.id)

        expected_response_data = OrderedDict(
            {
                "id": category.id,
                "name": category.name,
                "description": category.description,
                "tags": [
                    OrderedDict(
                        {
                            "id": tag.id,
                            "name": tag.name,
                        }
                    )
                    for tag in category.tags.all().order_by("id")
                ],
            }
        )

        assert 200 == response.status_code
        assert expected_response_data == response.data

    def test_api_response_on_successful_simple_fields_update(
        self,
        auth_request: Callable[
            [User, str, str, dict[str, Any] | None], APIRequestFactory
        ],
    ) -> None:
        user = UserFactory(is_active=True)
        category = CategoryFactory(created_by=user)

        request = auth_request(
            user,
            "PUT",
            f"api/categorization/categories/{category.id}/update",
            self.simple_field_data,
        )

        response = CategoryUpdateApi.as_view()(request, category.id)

        expected_response_data = OrderedDict(
            {
                "id": category.id,
                **self.simple_field_data,
                "tags": [
                    OrderedDict(
                        {
                            "id": tag.id,
                            "name": tag.name,
                        }
                    )
                    for tag in category.tags.all().order_by("id")
                ],
            }
        )

        assert 200 == response.status_code
        assert expected_response_data == response.data
