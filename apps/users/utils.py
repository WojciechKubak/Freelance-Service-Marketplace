from django.core.signing import TimestampSigner
from django.core.signing import BadSignature, SignatureExpired

# todo: replace with timezone.timedelta
from datetime import timedelta


def sign_user_id(id_: str) -> str:
    signer = TimestampSigner()
    return signer.sign(id_)


def unsign_user_id(
    signed_id: str, max_age: int | timedelta | None = None
) -> str | None:
    signer = TimestampSigner()
    try:
        return signer.unsign(signed_id, max_age=max_age)
    except (SignatureExpired, BadSignature):
        return None
