from apps.users.models import User
from apps.users.services import UserService, UserEmailService as EmailService
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.contrib import admin, messages
from django.http import HttpRequest
from collections import defaultdict


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

    actions = ("resend_activation_email", "send_password_reset_email")

    def save_model(self, request: HttpRequest, obj: User, form, change: bool) -> None:
        if change:
            return super().save_model(request, obj, form, change)

        try:
            UserService.user_create(**form.cleaned_data)
        except ValidationError as exc:
            self.message_user(request, str(exc), messages.ERROR)

    @admin.action(description="Resend activation email")
    def resend_activation_email(self, request: HttpRequest, queryset: QuerySet) -> None:
        errors = defaultdict(int)

        for user in queryset:
            try:
                EmailService.user_activation_email_send(email=user.email)
            except ValidationError as e:
                errors[e.message] += 1

        if errors:
            for message, count in errors.items():
                self.message_user(
                    request, f"{message} for {count} users", messages.ERROR
                )

        correct_count = queryset.count() - sum(errors.values())
        if correct_count:
            self.message_user(
                request, f"Activation email resent for {correct_count} users"
            )

    @admin.action(description="Password reset")
    def send_password_reset_email(
        self, request: HttpRequest, queryset: QuerySet
    ) -> None:
        errors = defaultdict(int)

        for user in queryset:
            try:
                EmailService.user_reset_password_email_send(email=user.email)
            except ValidationError as e:
                errors[e.message] += 1

        if errors:
            for message, count in errors.items():
                self.message_user(
                    request, f"{message} for {count} users", messages.ERROR
                )

        correct_count = queryset.count() - sum(errors.values())
        if correct_count:
            self.message_user(
                request, f"Password reset email sent for {correct_count} users"
            )
