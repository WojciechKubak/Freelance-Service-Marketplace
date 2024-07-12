from apps.users.models import User
from django.contrib import admin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "is_admin", "created_at", "updated_at")

    list_filter = ("is_admin", "is_active", "is_superuser")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_admin", "is_superuser")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    search_fields = ("email",)
    ordering = ("email",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )
