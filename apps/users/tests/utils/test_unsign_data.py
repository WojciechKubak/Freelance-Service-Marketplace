from django.core.signing import TimestampSigner
from apps.users.utils import unsign_data


class TestUnsignValue:

    def test_unsign_value_on_failed_do_to_signature_expired(self) -> None:
        signer = TimestampSigner()
        value = "test_value"
        signed_value = signer.sign(value)

        result = unsign_data(signed_value, max_age=-1)

        assert result is None

    def test_unsign_value_on_failed_do_to_bas_signature(self) -> None:
        signer = TimestampSigner()
        value = "test_value"
        signed_value = signer.sign(value)[:-1]

        result = unsign_data(signed_value)

        assert result is None

    def test_unsign_value_on_success(self) -> None:
        signer = TimestampSigner()
        value = "test_value"
        signed_value = signer.sign(value)

        result = unsign_data(signed_value)

        assert value == result
