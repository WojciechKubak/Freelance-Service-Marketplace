from django.core.signing import TimestampSigner
from apps.users.utils import sign_user_id


def test_sign_user_id_on_successed_value_signing() -> None:
    value = "test_value"

    signed_value = sign_user_id(value)

    signer = TimestampSigner()
    unsigned_value = signer.unsign(signed_value)

    assert value == unsigned_value
