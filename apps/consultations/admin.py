from apps.consultations.models import Consultation, Slot, Booking
from apps.consultations.services.bookings import BookingService
from apps.consultations.services.slots import SlotService
from apps.consultations.services.consultations import (
    consultation_change_visibility,
    consultation_create,
    consultation_update,
)
from django.core.exceptions import ValidationError
from django.contrib.admin import ModelAdmin
from django.db.models.query import QuerySet
from django.contrib import admin, messages
from django.forms import BaseModelForm
from django.http import HttpRequest
from django.forms.models import BaseInlineFormSet
from django import forms
from typing import Any


class ConsultationForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Consultation
        fields = ["title", "price", "content", "tags"]


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    form = ConsultationForm

    list_display = (
        "title",
        "price",
        "is_visible",
        "created_at",
        "updated_at",
    )

    list_filter = ("is_visible",)

    search_fields = ("title",)
    ordering = ("title", "price")

    readonly_fields = ("created_at", "updated_at")

    actions = ("consultation_change_visibility",)

    @admin.action(description="Change visibility of selected consultations")
    def consultation_change_visibility(
        modeladmin: ModelAdmin, request: HttpRequest, queryset: QuerySet[Any]
    ) -> None:
        for consultation in queryset:
            consultation_change_visibility(
                consultation=consultation, is_visible=not consultation.is_visible
            )
        modeladmin.message_user(
            request,
            "Selected consultations' visibility has been changed.",
            messages.SUCCESS,
        )

    def save_related(
        self,
        request: HttpRequest,
        form: BaseModelForm,
        formsets: BaseInlineFormSet,
        change: bool,
    ) -> None:
        # prevent from calling m2m save method
        pass

    def save_model(
        self, request: HttpRequest, obj: Consultation, form: BaseModelForm, change: bool
    ) -> None:
        try:
            (
                consultation_update(consultation=obj, **form.cleaned_data)
                if change
                else consultation_create(user=request.user, **form.cleaned_data)
            )
        except ValidationError as exc:
            self.message_user(request, str(exc), messages.ERROR)


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = (
        "consultation__title",
        "start_time",
        "end_time",
        "created_at",
        "updated_at",
        "is_cancelled",
    )

    search_fields = ("consultation__title",)
    ordering = ("start_time",)

    fieldsets = (
        (None, {"fields": ("consultation", "start_time", "end_time")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    readonly_fields = ("created_at", "updated_at")

    def save_model(
        self, request: HttpRequest, obj: Slot, form: BaseModelForm, change: bool
    ) -> None:
        try:
            consultation = obj.consultation
            slot_service = SlotService(consultation=consultation)

            if change:
                # todo: need to display content in the form
                slot_service.slot_update(
                    slot=obj,
                    start_time=form.cleaned_data.get("start_time"),
                    end_time=form.cleaned_data.get("end_time"),
                )
            else:
                slot_service.slot_create(
                    start_time=form.cleaned_data.get("start_time"),
                    end_time=form.cleaned_data.get("end_time"),
                )
        except ValidationError as exc:
            self.message_user(request, str(exc), messages.ERROR)


def delete_model(self, request: HttpRequest, obj: Slot) -> None:
    consultation = obj.consultation
    slot_service = SlotService(consultation=consultation)
    slot_service.slot_delete(slot=obj)
    self.message_user(request, "Slot deleted successfully.", messages.SUCCESS)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "slot__consultation__title",
        "booked_by",
        "start_time",
        "end_time",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (None, {"fields": ("slot", "booked_by", "start_time", "end_time")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    readonly_fields = ("created_at", "updated_at")

    search_fields = ("slot__consultation__title", "booked_by__email")

    ordering = ("start_time",)

    def save_model(
        self, request: HttpRequest, obj: Booking, form: BaseModelForm, change: bool
    ) -> None:
        try:
            slot = obj.slot
            booking_service = BookingService(slot=slot)
            booking_service.booking_create(
                user=obj.booked_by, start_time=obj.start_time, end_time=obj.end_time
            )
            self.message_user(
                request, "Booking created successfully.", messages.SUCCESS
            )
        except ValidationError as exc:
            self.message_user(request, str(exc), messages.ERROR)
