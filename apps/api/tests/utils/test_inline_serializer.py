from apps.api.utils import inline_serializer
from rest_framework import serializers


class TestInlineSerializer:

    def test_inline_serializer_creates_serializer_instance(self) -> None:
        serializer = inline_serializer(fields={"foo": serializers.CharField()})
        assert isinstance(serializer, serializers.Serializer)

    def test_inline_serializer_passes_kwargs(self) -> None:
        serializer = inline_serializer(
            fields={"foo": serializers.CharField()}, many=True
        )
        assert serializer.many is True

    def test_inline_serializer_passes_data(self) -> None:
        serializer = inline_serializer(
            fields={"foo": serializers.CharField()}, data={"foo": "bar"}
        )
        assert serializer.is_valid() is True
        assert serializer.validated_data == {"foo": "bar"}
