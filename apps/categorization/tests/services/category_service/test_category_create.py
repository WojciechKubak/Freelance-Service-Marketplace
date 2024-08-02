from apps.categorization.tests.factories import TagFactory, UserFactory, Category
from apps.categorization.services import CategoryService
import pytest


@pytest.mark.django_db
def test_create_category_creates_instance_with_expected_data_and_returns_it() -> None:
    data = {
        "name": "Test Category",
        "description": "Test Description",
        "tags": [tag.id for tag in TagFactory.create_batch(3)],
        "user": UserFactory(),
    }

    result = CategoryService.category_create(**data)

    assert Category.objects.get(id=result.id) == result

    assert data["name"] == result.name
    assert data["description"] == result.description
    assert data["user"].id == str(result.created_by.id)
    assert data["tags"] == list(result.tags.values_list("id", flat=True))
