import pytest

from vec64 import base64_symbol_indexes

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


@pytest.mark.parametrize(
    "convert_to_bytes",
    (False, True))
@pytest.mark.parametrize(
    "extra_input,expect_output",
    (("", bytes(range(64))),
     ("=", bytes(range(65))),
     ("==", bytes(range(65)) + bytes([64])),
     ("===", bytes(range(65)) + bytes([64])),
     ("*", bytes(range(64))),
     ("*=", bytes(range(64))),
     ("=*=", bytes(range(65))),
     ))
def test_base64_symbol_indexes(extra_input, convert_to_bytes, expect_output):
    input_text = f"{ALPHABET}{extra_input}"
    if convert_to_bytes:
        input_text = input_text.encode("us-ascii")
    assert base64_symbol_indexes(input_text) == expect_output
