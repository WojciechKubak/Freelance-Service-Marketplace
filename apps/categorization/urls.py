from apps.categorization.apis import (
    CategoryListApi,
)
from django.urls import path, include


category_patterns = [
    path("", CategoryListApi.as_view(), name="category-list"),
]


urlpatterns = [
    path(
        "categories/",
        include((category_patterns, "categories"), namespace="categories"),
    ),
]
