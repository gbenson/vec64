from dataclasses import dataclass, field
from enum import Enum

from _vec64 import (
    _RT_ALNUM,
    _RT_ALPHA,
    _RT_ALPHAHEX,
    _RT_BASE64,
    _RT_DECIMAL,
    _RT_HEX,
    _RT_LOWER,
    _RT_LOWER_ALNUM,
    _RT_LOWER_ALPHAHEX,
    _RT_LOWERHEX,
    _RT_PUNCT,
    _RT_UPPER,
    _RT_UPPER_ALNUM,
    _RT_UPPER_ALPHAHEX,
    _RT_UPPERHEX,
)


class CharType(Enum):
    ALPHA = _RT_ALPHA  # A-Za-z
    UPPER = _RT_UPPER  # A-Z
    LOWER = _RT_LOWER  # a-z

    ALNUM = _RT_ALNUM              # A-Za-z0-9
    UPPER_ALNUM = _RT_UPPER_ALNUM  # A-Z0-9
    LOWER_ALNUM = _RT_LOWER_ALNUM  # a-z0-9

    HEX = _RT_HEX            # A-Fa-f0-9
    UPPERHEX = _RT_UPPERHEX  # A-F0-9
    LOWERHEX = _RT_LOWERHEX  # a-f0-9

    ALPHAHEX = _RT_ALPHAHEX              # A-Fa-f
    UPPER_ALPHAHEX = _RT_UPPER_ALPHAHEX  # A-F
    LOWER_ALPHAHEX = _RT_LOWER_ALPHAHEX  # a-f

    DECIMAL = _RT_DECIMAL  # 0-9
    PUNCT = _RT_PUNCT      # '+' and '/'
    BASE64 = _RT_BASE64    # Everything!

    def __and__(self, other: "CharType") -> "CharType":
        if not isinstance(other, CharType):
            raise TypeError(other)
        return type(self)(self.value & other.value)


CT = CharType


@dataclass
class CTypeInfo:
    ctype: CharType
    symbols: str
    exclusions: set["CTypeInfo"] = field(default_factory=set)

    def __post_init__(self):
        self._unit_probability = len(self.symbols) / 64

    def __hash__(self) -> int:
        tagged_excls = ((e.ctype.name, e) for e in self.exclusions)
        sorted_excls = tuple(e for _, e in sorted(tagged_excls))
        return hash((self.ctype, self.symbols, sorted_excls))

    def __add__(self, other: "CTypeInfo") -> "CTypeInfo":
        if not isinstance(other, CTypeInfo):
            raise TypeError(other)
        ssyms = set(self.symbols)
        osyms = set(other.symbols)
        if ssyms.issuperset(osyms):
            raise ValueError(other)
        return type(self)(
            self.ctype & other.ctype,
            self.symbols + "".join(sorted(osyms.difference(ssyms))),
            {self, other} | self.exclusions | other.exclusions,
        )

    def __sub__(self, other: "CTypeInfo") -> "CTypeInfo":
        if not isinstance(other, CTypeInfo):
            raise TypeError(other)
        if not set(self.symbols).issuperset(set(other.symbols)):
            raise ValueError(other)
        return type(self)(
            self.ctype & other.ctype,
            self.symbols,
            {other} | self.exclusions | other.exclusions,
        )

    def probability(self, length: int) -> float:
        """Calculate probabilities of spans having this ctype.
        """
        return (self._unit_probability ** length) - sum(
            exclusion.probability(length) for exclusion in self.exclusions)


# Disjoint types
CI_UPPER_ALPHAHEX = CTypeInfo(CT.UPPER_ALPHAHEX, "ABCDEF")
CI_LOWER_ALPHAHEX = CTypeInfo(CT.LOWER_ALPHAHEX, "abcdef")
CI_DECIMAL = CTypeInfo(CT.DECIMAL, "0123456789")
CI_PUNCT = CTypeInfo(CT.PUNCT, "+/")

# Types which combine a disjoint type with an unclassified type
CI_UPPER = CTypeInfo(CT.UPPER, "ABCDEFGHIJKLMNOPQRSTUVWXYZ")-CI_UPPER_ALPHAHEX
CI_LOWER = CTypeInfo(CT.LOWER, "abcdefghijklmnopqrstuvwxyz")-CI_LOWER_ALPHAHEX

# Types which combine two disjoint types
CI_ALPHAHEX = CI_UPPER_ALPHAHEX + CI_LOWER_ALPHAHEX
CI_UPPERHEX = CI_DECIMAL + CI_UPPER_ALPHAHEX
CI_LOWERHEX = CI_DECIMAL + CI_LOWER_ALPHAHEX

# Types which combine compound types
CI_HEX = (CI_UPPERHEX + CI_LOWERHEX) - CI_ALPHAHEX
CI_ALPHA = (CI_UPPER + CI_LOWER) - CI_ALPHAHEX

CI_UPPER_ALNUM = (CI_UPPER + CI_DECIMAL) - CI_UPPERHEX
CI_LOWER_ALNUM = (CI_LOWER + CI_DECIMAL) - CI_LOWERHEX
CI_ALNUM = (CI_UPPER_ALNUM + CI_LOWER_ALNUM) - CI_ALPHA - CI_HEX

CI_BASE64 = CI_ALNUM + CI_PUNCT


ctype_info = dict(
    (ct, globals()[f"CI_{ct.name}"])
    for ct in CharType
)
