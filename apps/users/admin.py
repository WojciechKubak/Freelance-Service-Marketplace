from apps.users.models import User
from django.core.exceptions import ValidationError
from django.contrib import admin, messages
from django.http import HttpRequest
from apps.users.services import UserService


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "is_active",
        "is_admin",
        "is_superuser",
        "created_at",
        "updated_at",
    )

    list_filter = ("is_admin", "is_active", "is_superuser")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_admin", "is_superuser")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    search_fields = ("email",)
    ordering = ("email",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    def save_model(self, request: HttpRequest, obj: User, form, change: bool) -> None:
        if change:
            return super().save_model(request, obj, form, change)

        try:
            UserService.user_create(**form.cleaned_data)
        except ValidationError as exc:
            self.message_user(request, str(exc), messages.ERROR)
