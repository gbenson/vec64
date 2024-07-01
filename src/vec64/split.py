from typing import Optional

from _vec64 import _split
from .ctype import CharType, CT
from .span import Span


def split(
        sequence: bytes,
        sep: Optional[CharType] = CT.PUNCT,
        maxsplit: Optional[int] = -1,
) -> list[Span]:
    """Return a list of typed ranges in the input sequence.

    :param sequence:
        A bytes-like object of Base64 alphabet symbol indexes, as
        returned by `base64_symbol_indexes`.
    :param sep:
        The character type used to split the string.
    :param maxsplit:
        Maximim number of splits, starting from the left.  Values
        less than one mean no limit.
    """
    sep = getattr(sep, "value", -1)
    return [
        Span(start, limit, CharType(ctype))
        for start, limit, ctype in _split(sequence, maxsplit, sep)
    ]
