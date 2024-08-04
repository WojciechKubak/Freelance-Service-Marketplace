from apps.common.models import BaseModel
from apps.users.models import User
from django.db import models


# todo: add name field unique constraint + tests


class Category(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name


class Tag(BaseModel):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, related_name="tags", on_delete=models.CASCADE
    )

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
