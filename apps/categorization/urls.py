from apps.categorization.apis import (
    CategoryListApi,
    CategoryDetailApi,
)
from django.urls import path, include


category_patterns = [
    path("", CategoryListApi.as_view(), name="category-list"),
    path("<int:category_id>/", CategoryDetailApi.as_view(), name="category-detail"),
]


urlpatterns = [
    path(
        "categories/",
        include((category_patterns, "categories"), namespace="categories"),
    ),
]
