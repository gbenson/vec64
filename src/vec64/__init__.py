from deprecated import deprecated

from .ctype import CharType, CT
from .span import Span
from .wrappers import split, vectorize

__all__ = [
    "CharType",
    "Span",
    "split",
    "vectorize",
]


@deprecated(reason="'base64_symbol_indexes' has been renamed as 'vectorize'")
def base64_symbol_indexes(*args, **kwargs):
    return vectorize(*args, **kwargs)
