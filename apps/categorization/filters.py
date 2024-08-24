from apps.categorization.models import Tag
from django_filters.rest_framework import FilterSet


class TagFilter(FilterSet):
    class Meta:
        model = Tag
        fields = ["id", "name"]
