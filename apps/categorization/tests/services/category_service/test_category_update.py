from apps.categorization.tests.factories import CategoryFactory, TagFactory, Category
from apps.categorization.services import CategoryService
import pytest


class TestCategoryUpdate:

    @pytest.mark.django_db
    def test_category_update_on_simple_fields_data(self) -> None:
        category = CategoryFactory()

        update_data = {
            "name": f"new_{category.name}",
            "description": f"new_{category.description}",
        }

        result = CategoryService.category_update(category=category, **update_data)

        category = Category.objects.get(id=category.id)

        assert category == result

    @pytest.mark.django_db
    def test_category_update_on_m2m_tags_field_data(self) -> None:
        tags = TagFactory.create_batch(3)
        *existing, new = tags
        category = CategoryFactory(tags=existing)

        result = CategoryService.category_update(category=category, tags=[new.id])

        category = Category.objects.get(id=category.id)

        assert category == result
