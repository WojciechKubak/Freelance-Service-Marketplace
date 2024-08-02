from apps.categorization.models import Category
from apps.users.models import User
from dataclasses import dataclass


@dataclass
class CategoryService:

    @staticmethod
    def category_update(
        *,
        category: Category,
        name: str | None = None,
        description: str | None = None,
        tags: list[int] | None = None
    ) -> Category:
        category.name = name if name else category.name
        category.description = description if description else category.description

        if tags:
            existing_tags = set(category.tags.values_list("id", flat=True))
            combined_tags = existing_tags.union(tags)

            category.tags.set(combined_tags)

        category.full_clean()
        category.save()

        return category

    @staticmethod
    def category_create(
        *, user: User, name: str, description: str, tags: list[int]
    ) -> Category:
        category = Category(name=name, description=description, created_by=user)

        category.full_clean()
        category.save()

        category.tags.set(tags)

        return category
