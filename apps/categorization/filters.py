from apps.categorization.models import Tag

# todo: might change this to drf supported filters
from django_filters import FilterSet


class TagFilter(FilterSet):
    class Meta:
        model = Tag
        fields = ["id", "name"]
