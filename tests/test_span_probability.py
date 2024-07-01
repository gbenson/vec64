import pytest

from vec64 import Span, CT


@pytest.mark.parametrize(
    "ctype,expect_probability",
    ((CT.UPPER_ALPHAHEX, 6/64),
     (CT.LOWER_ALPHAHEX, 6/64),
     (CT.DECIMAL, 10/64),
     (CT.PUNCT, 2/64),
     (CT.UPPER, 20/64),
     (CT.LOWER, 20/64),
     (CT.UPPERHEX, 0),
     (CT.LOWERHEX, 0),
     (CT.ALPHAHEX, 0),
     (CT.ALPHA, 0),
     (CT.ALNUM, 0),
     (CT.UPPER_ALNUM, 0),
     (CT.LOWER_ALNUM, 0),
     (CT.HEX, 0),
     (CT.BASE64, 0),
     ))
def test_one_symbol_probability(ctype, expect_probability):
    """Check the probabilities of one-character spans are as expected.
    """
    span = Span(0, 1, ctype)
    assert span.probability == expect_probability


@pytest.mark.parametrize(
    "ctype,expect_probability",
    ((CT.UPPER_ALPHAHEX, (6/64)**2),
     (CT.LOWER_ALPHAHEX, (6/64)**2),
     (CT.DECIMAL, (10/64)**2),
     (CT.PUNCT, (2/64)**2),
     (CT.UPPER, (20/64)/2),  # (26*26 - 6*6)/(64*64) = 640/(64*64) = 10/64
     (CT.LOWER, (20/64)/2),  # (26*26 - 6*6)/(64*64) = 640/(64*64) = 10/64
     (CT.UPPERHEX, 2*(6/64 * 10/64)),
     (CT.LOWERHEX, 2*(6/64 * 10/64)),
     (CT.ALPHAHEX, 2*((6/64)**2)),
     (CT.ALPHA, 2*(6/64 * 20/64 + 20/64 * 26/64)),
     (CT.UPPER_ALNUM, 2*(20/64 * 10/64)),
     (CT.LOWER_ALNUM, 2*(20/64 * 10/64)),
     (CT.BASE64, 2*(2/64 * 62/64)),
     (CT.ALNUM, 0),
     (CT.HEX, 0),
     ))
def test_two_symbol_probability(ctype, expect_probability):
    """Check the probabilities of two-character spans are as expected.
    """
    span = Span(0, 2, ctype)
    assert span.probability == expect_probability


@pytest.mark.parametrize(
    "ctype,expect_probability",
    ((CT.UPPER_ALPHAHEX, (6/64)**3),
     (CT.LOWER_ALPHAHEX, (6/64)**3),
     (CT.DECIMAL, (10/64)**3),
     (CT.PUNCT, (2/64)**3),
     (CT.UPPER, (20/64)**3
      + 3*((20/64)**2 * 6/64)
      + 3*((6/64)**2 * 20/64)),
     (CT.LOWER, (20/64)**3
      + 3*((20/64)**2 * 6/64)
      + 3*((6/64)**2 * 20/64)),
     (CT.UPPERHEX, 3*((10/64)**2 * 6/64) + 3*((6/64)**2 * 10/64)),
     (CT.LOWERHEX, 3*((10/64)**2 * 6/64) + 3*((6/64)**2 * 10/64)),
     (CT.ALPHAHEX, 6*((6/64)**3)),
     #(CT.ALPHA,
     #(CT.UPPER_ALNUM,
     #(CT.LOWER_ALNUM,
     (CT.BASE64, 3*(2/64 * 62/64)),
     (CT.ALNUM, 6*((10/64 * (26/64)**2) - (10/64 * (6/64)**2))),
     (CT.HEX, 6*(10/64 * (6/64)**2)),
     ))
def test_three_symbol_probability(ctype, expect_probability):
    """Check the probabilities of three-character spans are as expected.
    """
    span = Span(0, 3, ctype)
    assert span.probability == expect_probability
