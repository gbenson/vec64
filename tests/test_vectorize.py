import pytest

from vec64 import vectorize


@pytest.mark.parametrize(
    "args,kwargs,expect_vector",
    (([""], {}, ()),
     (["hello"], {}, (33, 30, 37, 37, 40)),
     ([], dict(s=b"hello"), (33, 30, 37, 37, 40)),
     (["hello world"], {}, (33, 30, 37, 37, 40)),
     (["hello="], {}, (33, 30, 37, 37, 40, 0)),
     (["hello="], {"pad_with": 64}, (33, 30, 37, 37, 40, 64)),
     (["hello=="], {}, (33, 30, 37, 37, 40, 0, 0)),
     (["hello==="], {}, (33, 30, 37, 37, 40, 0, 0)),
     ))
def test_vectorize(args, kwargs, expect_vector):
    assert vectorize(*args, **kwargs) == bytes(expect_vector)
