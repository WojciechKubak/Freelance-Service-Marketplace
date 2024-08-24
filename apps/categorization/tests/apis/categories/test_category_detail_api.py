from apps.categorization.tests.factories import CategoryFactory
from apps.categorization.apis.categories import CategoryDetailApi
from rest_framework.test import APIRequestFactory
from collections import OrderedDict


class TestCategoryDetailApi:
    url = "api/categorization/categories"

    def test_api_response_on_successfully_found_category(self) -> None:
        category = CategoryFactory()
        tags = sorted(category.tags.all(), key=lambda tag: tag.id)

        factory = APIRequestFactory()
        request = factory.get(f"{self.url}/{category.id}")

        response = CategoryDetailApi.as_view()(request, category.id)

        expected_response_data = OrderedDict(
            {
                "id": category.id,
                "name": category.name,
                "description": category.description,
                "tags": [OrderedDict({"id": tag.id, "name": tag.name}) for tag in tags],
            }
        )

        assert response.status_code == 200
        assert expected_response_data == response.data

    def test_api_response_on_category_not_found(self) -> None:
        factory = APIRequestFactory()
        request = factory.get(f"{self.url}/999")

        response = CategoryDetailApi.as_view()(request, 1)

        expected_response_data = {"detail": "Not found."}

        assert response.status_code == 404
        assert expected_response_data == response.data
