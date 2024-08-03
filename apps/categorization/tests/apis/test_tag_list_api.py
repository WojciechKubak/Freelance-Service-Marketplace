from apps.categorization.tests.factories import TagFactory, CategoryFactory
from apps.categorization.apis import TagListApi
from rest_framework.test import APIRequestFactory
from collections import OrderedDict
import pytest


class TestTagListApi:

    @pytest.mark.django_db
    def test_api_response_with_no_filters_provided(self) -> None:
        tags = TagFactory.create_batch(2)
        tags = sorted(tags, key=lambda tag: tag.id)

        factory = APIRequestFactory()
        request = factory.get("api/categorization/tags/")

        response = TagListApi.as_view()(request)

        expected_response_data = [
            OrderedDict({"id": tag.id, "name": tag.name}) for tag in tags
        ]

        assert 200 == response.status_code
        assert response.data == expected_response_data

    @pytest.mark.django_db
    def test_api_response_on_single_simple_field_filter(self) -> None:
        tags = TagFactory.create_batch(2)
        tags = sorted(tags, key=lambda tag: tag.id)

        factory = APIRequestFactory()
        request = factory.get("api/categorization/tags/", {"id": tags[0].id})

        response = TagListApi.as_view()(request)

        expected_response_data = [OrderedDict({"id": tags[0].id, "name": tags[0].name})]

        assert 200 == response.status_code
        assert response.data == expected_response_data

    @pytest.mark.django_db
    def test_api_response_on_chained_simple_fields_filter(self) -> None:
        category = CategoryFactory()
        tags = TagFactory.create_batch(3, category=category)

        factory = APIRequestFactory()
        request = factory.get(
            "api/categorization/tags/",
            {"category": category.name, "name": tags[0].name},
        )

        response = TagListApi.as_view()(request)

        expected_response_data = [OrderedDict({"id": tags[0].id, "name": tags[0].name})]

        assert 200 == response.status_code
        assert response.data == expected_response_data
