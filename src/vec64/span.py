from collections import namedtuple

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

    @property
    def probability(self) -> float:
        """The probability a span of this length would have this ctype.
        """
        return self.ctype_info.probability(self.length)
