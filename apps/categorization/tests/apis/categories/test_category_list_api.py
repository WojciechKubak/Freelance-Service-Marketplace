from apps.categorization.tests.factories import CategoryFactory
from apps.categorization.apis.categories import CategoryListApi
from rest_framework.test import APIRequestFactory
from collections import OrderedDict
import pytest


@pytest.mark.django_db
def test_api_response_on_successfull_category_list() -> None:
    categories = CategoryFactory.create_batch(2)
    categories = sorted(categories, key=lambda category: category.id)

    factory = APIRequestFactory()
    request = factory.get("api/categorization/categories/")

    response = CategoryListApi.as_view()(request)

    expected_response_data = [
        OrderedDict({"id": category.id, "name": category.name})
        for category in categories
    ]

    assert response.status_code == 200
    assert expected_response_data == response.data
