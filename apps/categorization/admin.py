from apps.categorization.models import Category, Tag
from apps.categorization.services.category_service import CategoryService
from apps.categorization.services.tag_service import TagService
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.contrib import admin, messages
from django.forms import BaseModelForm
from django.http import HttpRequest


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (None, {"fields": ("name", "description")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    search_fields = ("name",)
    ordering = ("name",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        queryset = super().get_queryset(request)
        return queryset.defer("description")

    def save_model(
        self, request: HttpRequest, obj: Category, form: BaseModelForm, change: bool
    ) -> None:
        try:
            (
                CategoryService.category_update(category=obj, **form.cleaned_data)
                if change
                else CategoryService.category_create(
                    user=request.user, **form.cleaned_data
                )
            )
        except ValidationError as exc:
            self.message_user(request, str(exc), messages.ERROR)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (None, {"fields": ("name", "category")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    search_fields = ("name", "category__name")
    ordering = ("name",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        queryset = super().get_queryset(request)
        return queryset.defer("category__description")

    def save_model(
        self, request: HttpRequest, obj: Tag, form: BaseModelForm, change: bool
    ) -> None:
        try:
            category_instance = form.cleaned_data.pop("category")
            form.cleaned_data["category_id"] = category_instance.id

            (
                TagService.tag_update(tag=obj, **form.cleaned_data)
                if change
                else TagService.tag_create(user=request.user, **form.cleaned_data)
            )

        except ValidationError as exc:
            self.message_user(request, str(exc), messages.ERROR)
