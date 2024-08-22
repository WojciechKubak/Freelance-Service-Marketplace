from apps.categorization.models import Category, Tag
from apps.users.models import User
from django.core.exceptions import ValidationError


def tag_create(*, user: User, name: str, category_id: int) -> Tag:
    if not Category.objects.filter(id=category_id).exists():
        raise ValidationError("Category does not exist")

    tag = Tag(name=name, category_id=category_id, created_by=user)

    tag.full_clean()
    tag.save()

    return tag


@staticmethod
def tag_update(
    *,
    tag: Tag,
    name: str | None = None,
    category_id: int | None = None,
) -> Tag:
    if category_id:
        if not Category.objects.filter(id=category_id).exists():
            raise ValidationError("Category does not exist")
        tag.category_id = category_id

    tag.name = name if name else tag.name

    tag.full_clean()
    tag.save()

    return tag
