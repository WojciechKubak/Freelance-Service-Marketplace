from apps.categorization.models import Category
from apps.users.models import User


def category_update(
    *,
    category: Category,
    name: str | None = None,
    description: str | None = None,
) -> Category:
    category.name = name if name else category.name
    category.description = description if description else category.description

    category.full_clean()
    category.save()

    return category


def category_create(*, user: User, name: str, description: str) -> Category:
    category = Category(name=name, description=description, created_by=user)

    category.full_clean()
    category.save()

    return category
