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
