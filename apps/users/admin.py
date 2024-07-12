from apps.users.models import User
from django.contrib import admin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "is_admin")

    list_filter = ("is_admin", "is_active")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_admin", "is_superuser")}),
    )

    search_fields = ("email",)
    ordering = ("email",)
