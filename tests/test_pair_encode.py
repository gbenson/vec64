import pytest

from vec64 import vectorize, pair_encode


@pytest.mark.parametrize(
    "input_text,expect_encoded",
    (("AA",  0*64 + 0),
     # ..
     ("/A",  0*64 + 63),
     ("AB",  1*64 + 0),
     # ..
     ("/B",  1*64 + 63),
     # ..
     ("A/", 63*64 + 0),
     # ..
     ("//", 63*64 + 63),
     ("A=", 64*64 + 0),
     # ..
     ("/=", 64*64 + 63),
     ("==", 64*64 + 64),
     # ...and:
     ("Cj", 35*64 + 2),
     ("o=", 64*64 + 40),
     ))
def test_individual_pairs(input_text, expect_encoded):
    assert pair_encode(vectorize(input_text)) == (expect_encoded,)


@pytest.mark.parametrize(
    "input_text,kwargs,expect_output",
    (("", {}, ()),
     ("hello", {},
      ((30 << 6) | 33, (37 << 6) | 37)),
     ("hello=", {},
      ((30 << 6) | 33, (37 << 6) | 37, (64 << 6) | 40)),
     ("hello==", {},
      ((30 << 6) | 33, (37 << 6) | 37, (64 << 6) | 40)),
     ("hello", dict(start=1),
      ((37 << 6) | 30, (40 << 6) | 37)),
     ("hello=", dict(start=1),
      ((37 << 6) | 30, (40 << 6) | 37)),
     ("hello==", dict(start=1),
      ((37 << 6) | 30, (40 << 6) | 37, (64 << 6) | 64)),
     ))
def test_sequences(input_text, kwargs, expect_output):
    assert pair_encode(vectorize(input_text), **kwargs) == expect_output
