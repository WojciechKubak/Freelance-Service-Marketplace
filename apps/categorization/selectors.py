from apps.categorization.models import Tag
from apps.categorization.filters import TagFilter
from django.db.models import QuerySet


def tag_list(*, filters: dict[str, str | bool] = None) -> QuerySet:
    # todo: this list logic repeats in many places
    filters = filters or {}
    queryset = Tag.objects.all()

    return TagFilter(filters, queryset).qs
