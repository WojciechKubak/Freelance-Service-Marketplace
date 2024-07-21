from django.core.signing import TimestampSigner
from django.core.signing import BadSignature, SignatureExpired
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
