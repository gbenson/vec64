from itertools import permutations

import pytest

from vec64 import base64_symbol_indexes, split, RangeType as RT


@pytest.mark.parametrize(
    "input_text",
    ("".join(p) for p in permutations("AGag1+", 6)))
def test_all_transitions(input_text):
    """Any input sequences comprising one of each character type should
    come back as base64.  This ought to flex every possible transition.
    """
    ranges = split(base64_symbol_indexes(input_text), sep=-1)

    assert len(ranges) in range(2, 6)
    assert ranges[-1] == (0, 6, RT.BASE64)
    assert not any(r.start != 0 for r in ranges)
    assert not any(r.kind is RT.BASE64 for r in ranges[:-1])

    if (puncpos := input_text.find("+")) < 2:
        assert len(ranges) == 2
        assert ranges[0].limit == 1
        return

    assert 2 <= puncpos < 6
    assert len(ranges) >= min(puncpos, 3)
    assert len(ranges) <= puncpos + 1


@pytest.mark.parametrize(
    "input_text,expect_result",
    (("", []),
     # Range types
     ("A", [(0, 1, RT.UPPER_ALPHAHEX)]),
     ("G", [(0, 1, RT.UPPER)]),
     ("a", [(0, 1, RT.LOWER_ALPHAHEX)]),
     ("g", [(0, 1, RT.LOWER)]),
     ("1", [(0, 1, RT.DECIMAL)]),
     ("+", [(0, 1, RT.PUNCT)]),
     # Basic splits
     ("hello",
      [(0, 5, RT.LOWER),
       ]),
     ("/hello",
      [(0, 1, RT.PUNCT),
       (1, 6, RT.LOWER),
       ]),
     ("hello/",
      [(0, 5, RT.LOWER),
       (5, 6, RT.PUNCT),
       ]),
     ("/hello/",
      [(0, 1, RT.PUNCT),
       (1, 6, RT.LOWER),
       (6, 7, RT.PUNCT),
       ]),
     ("/hello/World4",
      [(0, 1, RT.PUNCT),
       (1, 6, RT.LOWER),
       (6, 7, RT.PUNCT),
       (7, 8, RT.UPPER),
       (7, 12, RT.ALPHA),
       (7, 13, RT.ALNUM),
       ]),
     ("/hello/World4/",
      [(0, 1, RT.PUNCT),
       (1, 6, RT.LOWER),
       (6, 7, RT.PUNCT),
       (7, 8, RT.UPPER),
       (7, 12, RT.ALPHA),
       (7, 13, RT.ALNUM),
       (13, 14, RT.PUNCT),
       ]),
     ))
def test_split(input_text, expect_result):
    assert split(base64_symbol_indexes(input_text)) == expect_result


@pytest.mark.parametrize(
    "input_text,expect_output",
    (("UklGRgoGAABXRUJQVlA4TP4FAAAvKgEQEIcAEIT",
      [(0,  1, RT.UPPER),
       (0, 19, RT.ALPHA),
       (0, 39, RT.ALNUM)]),
     ))
def test_regressions(input_text, expect_output):
    assert split(base64_symbol_indexes(input_text)) == expect_output
