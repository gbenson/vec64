import random

from collections import Counter
from itertools import pairwise

import pytest

from vec64 import (
    pair_encode,
    pair_decode,
    vectorize,
)


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


@pytest.mark.parametrize(
    "random_seed", (None, 23, 42, 186283)
)
def test_all_encodings(random_seed):
    pair_encoded = list(range(64*64 + 65))
    if random_seed is not None:
        random.seed(random_seed)
        random.shuffle(pair_encoded)
    pair_encoded = tuple(pair_encoded)
    print(repr(pair_encoded)[:80])
    assert len(pair_encoded) == 4161

    symbol_indexes = pair_decode(pair_encoded)
    print(repr(symbol_indexes)[:80])
    assert len(symbol_indexes) == 8322
    counts = Counter(
        bytes(pair)
        for i, pair in enumerate(pairwise(symbol_indexes))
        if not (i & 1)
    )
    assert len(counts) == 4161
    assert set(counts.values()) == {1}

    assert pair_encode(symbol_indexes) == pair_encoded
