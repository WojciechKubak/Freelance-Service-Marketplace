from apps.consultations.models import Booking
from apps.users.models import User
from django.db.models import QuerySet


def booking_list(*, user: User) -> QuerySet[Booking]:
    return Booking.objects.filter(booked_by=user)
