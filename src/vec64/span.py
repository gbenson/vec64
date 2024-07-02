from collections import namedtuple
from functools import cached_property

from .ctype import CTypeInfo, ctype_info


class Span(namedtuple("_Span", ("start", "limit", "ctype"))):
    @property
    def ctype_info(self) -> CTypeInfo:
        return ctype_info[self.ctype]

    @property
    def length(self) -> int:
        """The number of characters in this span.
        """
        return self.limit - self.start

    @cached_property
    def probability(self) -> float:
        """The probability of a span of this length having this ctype.
        """
        return self.ctype_info.probability(self.length)
