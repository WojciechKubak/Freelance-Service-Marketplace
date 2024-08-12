from apps.consultations.services import ConsultationService, SlotService, BookingService
from apps.consultations.models import Consultation, Slot
from apps.consultations.selectors import (
    ConsultationSelectors,
    SlotSelectors,
    BookingSelectors,
)
from apps.api.pagination import get_paginated_response
from apps.api.permissions import IsOwner
from apps.api.utils import inline_serializer
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import serializers
from rest_framework import status
from django.shortcuts import get_object_or_404


class ConsultationCreateApi(APIView):
    permission_classes = (IsAuthenticated,)

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField()
        description = serializers.CharField()
        price = serializers.FloatField()
        tags = serializers.ListField(
            child=serializers.IntegerField(), min_length=1, max_length=5
        )

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField()
        description = serializers.CharField()
        price = serializers.FloatField()
        tags = inline_serializer(
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
            },
            many=True,
        )

    def post(self, request: Request) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        consultation = ConsultationService.consultation_create(
            user=request.user, **input_serializer.validated_data
        )

        output_serializer = self.OutputSerializer(consultation)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class ConsultationUpdateApi(APIView):
    permission_classes = (IsOwner,)

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(required=False)
        description = serializers.CharField(required=False)
        price = serializers.FloatField(required=False)
        tags = serializers.ListField(child=serializers.IntegerField(), required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField()
        description = serializers.CharField()
        price = serializers.FloatField()
        tags = inline_serializer(
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
            },
            many=True,
        )

    def post(self, request: Request, consultation_id: int) -> Response:
        consultation = get_object_or_404(Consultation, id=consultation_id)

        self.check_object_permissions(request, consultation)

        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        consultation = ConsultationService.consultation_update(
            consultation, **input_serializer.validated_data
        )

        output_serializer = self.OutputSerializer(consultation)
        return Response(output_serializer.data)


class ConsultationChangeVisibilityApi(APIView):
    permission_classes = (IsOwner,)

    class InputSerializer(serializers.Serializer):
        is_visible = serializers.BooleanField(required=True)

    def patch(self, request: Request, consultation_id: int) -> Response:
        consultation = get_object_or_404(Consultation, id=consultation_id)
        self.check_object_permissions(request, consultation)

        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        ConsultationService.consultation_change_visibility(
            consultation, is_visible=input_serializer.validated_data["is_visible"]
        )

        return Response(status=status.HTTP_204_NO_CONTENT)


class ConsultationListApi(APIView):
    permission_classes = (AllowAny,)

    class Pagination(LimitOffsetPagination):
        default_limit = 20
        max_limit = 100
        page_size_query_param = "count"

    class FilterSerializer(serializers.Serializer):
        title = serializers.CharField(required=False)
        category_id = serializers.IntegerField(required=False)
        tag_id = serializers.IntegerField(required=False)
        price_min = serializers.FloatField(required=False)
        price_max = serializers.FloatField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField()
        price = serializers.FloatField()
        tags = inline_serializer(
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
            },
            many=True,
        )

    def get(self, request: Request) -> Response:
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        consultations = ConsultationSelectors.consultation_list(
            filters=filter_serializer.validated_data
        )

        # todo: missing pagination call here
        output_serializer = self.OutputSerializer(consultations, many=True)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class ConsultationDetailApi(APIView):
    permission_classes = (AllowAny,)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField()
        description = serializers.CharField()
        price = serializers.FloatField()
        tags = inline_serializer(
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
            },
            many=True,
        )

    def get(self, _: Request, consultation_id: int) -> Response:
        consultation = ConsultationSelectors.consultation_detail(
            consultation_id=consultation_id
        )

        output_serializer = self.OutputSerializer(consultation)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class SlotCreateApi(APIView):
    permission_classes = (IsOwner,)

    class InputSerializer(serializers.Serializer):
        consultation_id = serializers.IntegerField()
        start_time = serializers.DateTimeField()
        end_time = serializers.DateTimeField()

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        start_time = serializers.DateTimeField()
        end_time = serializers.DateTimeField()
        consultation = inline_serializer(
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
        )

    def post(self, request: Request) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        validated_data = input_serializer.validated_data

        consultation = get_object_or_404(
            Consultation, id=validated_data.pop("consultation_id")
        )

        self.check_object_permissions(request, consultation)

        slot = SlotService(consultation=consultation).slot_create(**validated_data)

        output_serializer = self.OutputSerializer(slot)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class SlotUpdateApi(APIView):
    permission_classes = (IsOwner,)

    class InputSerializer(serializers.Serializer):
        start_time = serializers.DateTimeField(required=False)
        end_time = serializers.DateTimeField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        start_time = serializers.DateTimeField()
        end_time = serializers.DateTimeField()

    def put(self, request: Request, slot_id: int) -> Response:
        slot = get_object_or_404(Slot, id=slot_id)
        consultation = slot.consultation

        self.check_object_permissions(request, consultation)

        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        slot = SlotService(consultation=consultation).slot_update(
            slot, **input_serializer.validated_data
        )

        output_serializer = self.OutputSerializer(slot)
        return Response(output_serializer.data)


class SlotDeleteApi(APIView):
    permission_classes = (IsOwner,)

    def delete(self, request: Request, slot_id: int) -> Response:
        slot = get_object_or_404(Slot, id=slot_id)
        consultation = slot.consultation

        self.check_object_permissions(request, consultation)

        SlotService(consultation=consultation).slot_delete(slot)

        return Response(status=status.HTTP_204_NO_CONTENT)


class SlotListApi(APIView):
    permission_classes = (AllowAny,)

    class Pagination(LimitOffsetPagination):
        default_limit = 20
        max_limit = 100
        page_size_query_param = "count"

    class FilterSerializer(serializers.Serializer):
        consultation_id = serializers.IntegerField(required=True)
        start_time = serializers.DateTimeField(required=False)
        end_time = serializers.DateTimeField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Slot
            fields = ["id", "start_time", "end_time"]

    def get(self, request: Request) -> Response:
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)

        slots = SlotSelectors.slot_list(filters=filter_serializer.validated_data)

        response = get_paginated_response(
            queryset=slots,
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            request=request,
        )

        return response


class SlotDetailApi(APIView):
    permission_classes = (AllowAny,)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        start_time = serializers.DateTimeField()
        end_time = serializers.DateTimeField()
        consultation = inline_serializer(
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
        )

    def get(self, _: Request, slot_id: int) -> Response:
        slot = SlotSelectors.slot_detail(slot_id=slot_id)
        output_serializer = self.OutputSerializer(slot)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


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
