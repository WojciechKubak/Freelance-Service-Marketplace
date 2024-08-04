from apps.categorization.apis import (
    CategoryListApi,
    CategoryDetailApi,
    CategoryUpdateApi,
    CategoryCreateApi,
    TagListApi,
    TagCreateApi,
    TagUpdateApi,
)
from django.urls import path, include


category_patterns = [
    path("", CategoryListApi.as_view(), name="category-list"),
    path("<int:category_id>/", CategoryDetailApi.as_view(), name="category-detail"),
    path(
        "<int:category_id>/update/", CategoryUpdateApi.as_view(), name="category-update"
    ),
    path("create/", CategoryCreateApi.as_view(), name="category-create"),
]

tag_patterns = [
    path("", TagListApi.as_view(), name="tag-list"),
    path("create/", TagCreateApi.as_view(), name="tag-create"),
    path("<int:tag_id>/update/", TagUpdateApi.as_view(), name="tag-update"),
]


urlpatterns = [
    path(
        "categories/",
        include((category_patterns, "categories"), namespace="categories"),
    ),
    path("tags/", include((tag_patterns, "tags"), namespace="tags")),
]
