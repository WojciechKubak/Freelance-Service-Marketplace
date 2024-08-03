from apps.categorization.models import Category, Tag
from apps.users.models import User
from django.core.exceptions import ValidationError
from dataclasses import dataclass


@dataclass
class CategoryService:

    @staticmethod
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

    @staticmethod
    def category_create(*, user: User, name: str, description: str) -> Category:
        category = Category(name=name, description=description, created_by=user)

        category.full_clean()
        category.save()

        return category


class TagService:

    @staticmethod
    def tag_create(*, user: User, name: str, category_id: int) -> Tag:
        if not Category.objects.filter(id=category_id).exists():
            raise ValidationError("Category does not exist")

        tag = Tag(name=name, category_id=category_id, created_by=user)

        tag.full_clean()
        tag.save()

        return tag
