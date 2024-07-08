from deprecated import deprecated

from _vec64 import pair_encode
from .ctype import CharType, CT
from .span import Span
from .wrappers import split, vectorize

__all__ = [
    "CharType",
    "Span",
    "pair_encode",
    "split",
    "vectorize",
]


@deprecated(reason="'base64_symbol_indexes' has been renamed as 'vectorize'")
def base64_symbol_indexes(*args, **kwargs):
    return vectorize(*args, **kwargs)
