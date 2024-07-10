import os
import random

from base64 import b64encode

import pytest

from vec64 import vectorize, unvectorize


@pytest.fixture
def input_data():
    topdir = os.path.dirname(os.path.dirname(__file__))
    with open(os.path.join(topdir, "LICENSE"), "r") as fp:
        return fp.read().encode("us-ascii")


@pytest.mark.parametrize("random_seed", (None, 23, 42, 186283))
def test_unvectorize(input_data, random_seed):
    assert len(input_data) == 11357
    if random_seed is not None:
        random.seed(random_seed)
        input_data = bytearray(input_data)
        random.shuffle(input_data)
    input_data = b64encode(input_data)
    assert len(input_data) == 15144

    symbol_indexes = vectorize(input_data)
    assert len(input_data) == len(input_data)

    print(repr(input_data)[:80])
    print(repr(tuple(symbol_indexes))[:80])

    assert unvectorize(symbol_indexes) == input_data.decode("us-ascii")
