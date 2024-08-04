from apps.categorization.tests.factories import CategoryFactory, Category
from apps.categorization.services.category_service import CategoryService
import pytest


@pytest.mark.django_db
def test_category_update_on_simple_fields_data() -> None:
    category = CategoryFactory()

    update_data = {
        "name": f"new_{category.name}",
        "description": f"new_{category.description}",
    }

    result = CategoryService.category_update(category=category, **update_data)

    category = Category.objects.get(id=category.id)

    assert category == result
