from django.core.signing import TimestampSigner
from apps.users.utils import sign_data


def test_sign_data_on_successed_value_signing() -> None:
    value = "test_value"

    signed_value = sign_data(value)

    signer = TimestampSigner()
    unsigned_value = signer.unsign(signed_value)

    assert value == unsigned_value
