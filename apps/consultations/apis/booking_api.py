from apps.consultations.services import BookingService
from apps.consultations.models import Slot
from apps.consultations.selectors import BookingSelectors
from apps.api.utils import inline_serializer
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404


class BookingCreateApi(APIView):
    permission_classes = (IsAuthenticated,)

    class InputSerializer(serializers.Serializer):
        slot_id = serializers.IntegerField()
        start_time = serializers.DateTimeField()
        end_time = serializers.DateTimeField()

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        start_time = serializers.DateTimeField()
        end_time = serializers.DateTimeField()
        slot = inline_serializer(
            fields={
                "id": serializers.IntegerField(),
                "start_time": serializers.DateTimeField(),
                "end_time": serializers.DateTimeField(),
                "consultation": inline_serializer(
                    fields={
                        "id": serializers.IntegerField(),
                        "title": serializers.CharField(),
                        "price": serializers.FloatField(),
                        "tags": inline_serializer(
                            fields={
                                "id": serializers.IntegerField(),
                                "name": serializers.CharField(),
                            },
                            many=True,
                        ),
                    }
                ),
            }
        )

    def post(self, request: Request) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        validated_data = input_serializer.validated_data

        slot = get_object_or_404(Slot, id=validated_data.pop("slot_id"))

        booking = BookingService(slot=slot).booking_create(
            user=request.user, **validated_data
        )

        output_serializer = self.OutputSerializer(booking)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class BookingListApi(APIView):
    permission_classes = (IsAuthenticated,)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        start_time = serializers.DateTimeField()
        end_time = serializers.DateTimeField()
        slot = inline_serializer(
            fields={
                "id": serializers.IntegerField(),
                "consultation": inline_serializer(
                    fields={
                        "id": serializers.IntegerField(),
                        "title": serializers.CharField(),
                        "created_by": inline_serializer(
                            fields={
                                "id": serializers.CharField(),
                                "email": serializers.CharField(),
                            }
                        ),
                    }
                ),
            }
        )

    def get(self, request: Request) -> Response:
        bookings = BookingSelectors.booking_list(user=request.user)

        output_serializer = self.OutputSerializer(bookings, many=True)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
