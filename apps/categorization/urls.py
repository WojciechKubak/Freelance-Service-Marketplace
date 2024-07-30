from apps.categorization.apis import (
    CategoryListApi,
    CategoryDetailApi,
    CategoryUpdateApi,
)
from django.urls import path, include


category_patterns = [
    path("", CategoryListApi.as_view(), name="category-list"),
    path("<int:category_id>/", CategoryDetailApi.as_view(), name="category-detail"),
    path(
        "<int:category_id>/update/", CategoryUpdateApi.as_view(), name="category-update"
    ),
]


urlpatterns = [
    path(
        "categories/",
        include((category_patterns, "categories"), namespace="categories"),
    ),
]
