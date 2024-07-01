from itertools import permutations

import pytest

from vec64 import base64_symbol_indexes, split, CT


@pytest.mark.parametrize(
    "input_text",
    ("".join(p) for p in permutations("AGag1+", 6)))
def test_all_transitions(input_text):
    """Any input sequences comprising one of each character type should
    come back as base64.  This ought to flex every possible transition.
    """
    spans = split(base64_symbol_indexes(input_text), sep=-1)

    assert len(spans) in range(2, 6)
    assert spans[-1] == (0, 6, CT.BASE64)
    assert not any(span.start != 0 for span in spans)
    assert not any(span.ctype is CT.BASE64 for span in spans[:-1])

    if (puncpos := input_text.find("+")) < 2:
        assert len(spans) == 2
        assert spans[0].limit == 1
        return

    assert 2 <= puncpos < 6
    assert len(spans) >= min(puncpos, 3)
    assert len(spans) <= puncpos + 1


@pytest.mark.parametrize(
    "input_text,expect_result",
    (("", []),
     # Character types
     ("A", [(0, 1, CT.UPPER_ALPHAHEX)]),
     ("G", [(0, 1, CT.UPPER)]),
     ("a", [(0, 1, CT.LOWER_ALPHAHEX)]),
     ("g", [(0, 1, CT.LOWER)]),
     ("1", [(0, 1, CT.DECIMAL)]),
     ("+", [(0, 1, CT.PUNCT)]),
     # Basic splits
     ("hello",
      [(0, 5, CT.LOWER),
       ]),
     ("/hello",
      [(0, 1, CT.PUNCT),
       (1, 6, CT.LOWER),
       ]),
     ("hello/",
      [(0, 5, CT.LOWER),
       (5, 6, CT.PUNCT),
       ]),
     ("/hello/",
      [(0, 1, CT.PUNCT),
       (1, 6, CT.LOWER),
       (6, 7, CT.PUNCT),
       ]),
     ("/hello/World4",
      [(0, 1, CT.PUNCT),
       (1, 6, CT.LOWER),
       (6, 7, CT.PUNCT),
       (7, 8, CT.UPPER),
       (7, 12, CT.ALPHA),
       (7, 13, CT.ALNUM),
       ]),
     ("/hello/World4/",
      [(0, 1, CT.PUNCT),
       (1, 6, CT.LOWER),
       (6, 7, CT.PUNCT),
       (7, 8, CT.UPPER),
       (7, 12, CT.ALPHA),
       (7, 13, CT.ALNUM),
       (13, 14, CT.PUNCT),
       ]),
     ))
def test_split(input_text, expect_result):
    assert split(base64_symbol_indexes(input_text)) == expect_result


@pytest.mark.parametrize(
    "input_text,expect_output",
    (("UklGRgoGAABXRUJQVlA4TP4FAAAvKgEQEIcAEIT",
      [(0,  1, CT.UPPER),
       (0, 19, CT.ALPHA),
       (0, 39, CT.ALNUM)]),
     ))
def test_regressions(input_text, expect_output):
    assert split(base64_symbol_indexes(input_text)) == expect_output
