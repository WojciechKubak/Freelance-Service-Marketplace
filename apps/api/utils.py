from rest_framework import serializers
from typing import Any, Optional


def _create_serializer_class(
    name: str, fields: dict[str, Any]
) -> type[serializers.Serializer]:
    return type(name, (serializers.Serializer,), fields)


def inline_serializer(
    *,
    fields: dict[str, Any],
    data: Optional[dict[str, Any]] = None,
    **kwargs: dict[str, Any]
) -> serializers.Serializer:
    serializer_class = _create_serializer_class(name="inline_serializer", fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)
