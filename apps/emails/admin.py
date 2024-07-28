from apps.emails.models import Email
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.contrib import admin


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ("id", "to", "subject", "status", "sent_at")

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        queryset = super().get_queryset(request)
        return queryset.defer("html", "plain_text")
