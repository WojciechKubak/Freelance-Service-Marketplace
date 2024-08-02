from apps.common.models import BaseModel
from apps.users.models import User
from django.db import models


# todo: add name field unique constraint + tests


class Category(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField("Tag", related_name="categories", blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"(Category: {self.name})"


class Tag(BaseModel):
    name = models.CharField(max_length=100)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"(Tag: {self.name})"
