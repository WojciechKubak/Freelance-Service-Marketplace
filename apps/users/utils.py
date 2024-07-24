from django.core.signing import TimestampSigner
from django.core.signing import BadSignature, SignatureExpired
from django.urls import reverse
from django.conf import settings
from datetime import timedelta


def sign_data(value: str) -> str:
    signer = TimestampSigner()
    return signer.sign(value)


def unsign_data(
    signed_value: str, max_age: int | timedelta | None = None
) -> str | None:
    signer = TimestampSigner()
    try:
        return signer.unsign(signed_value, max_age=max_age)
    except (SignatureExpired, BadSignature):
        return None


def url_generate(*, user_id: str, viewname: str) -> str:
    signed_id = sign_data(user_id)
    url = reverse(viewname, kwargs={"signed_id": signed_id})

    return f"{settings.BASE_BACKEND_URL}{url}"
