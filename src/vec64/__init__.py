from _vec64 import pair_encode
from .ctype import CharType, CT
from .span import Span
from .util import ALPHABET, pair_decode, unvectorize
from .wrappers import base64_symbol_indexes, split

vectorize = base64_symbol_indexes

__all__ = [
    "ALPHABET",
    "CharType",
    "Span",
    "base64_symbol_indexes",
    "pair_decode",
    "pair_encode",
    "split",
    "vectorize",
    "unvectorize",
]
