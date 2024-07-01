import pytest

import _vec64


@pytest.mark.parametrize(
    "a,b,expect_result",
    (("UPPER_ALPHAHEX", "UPPER",          "UPPER"),
     ("UPPER_ALPHAHEX", "LOWER_ALPHAHEX", "ALPHAHEX"),
     ("UPPER_ALPHAHEX", "LOWER",          "ALPHA"),
     ("UPPER_ALPHAHEX", "DECIMAL",        "UPPERHEX"),
     ("UPPER_ALPHAHEX", "PUNCT",          "BASE64"),

     ("UPPER",          "LOWER_ALPHAHEX", "ALPHA"),
     ("UPPER",          "LOWER",          "ALPHA"),
     ("UPPER",          "DECIMAL",        "UPPER_ALNUM"),
     ("UPPER",          "PUNCT",          "BASE64"),

     ("LOWER_ALPHAHEX", "LOWER",          "LOWER"),
     ("LOWER_ALPHAHEX", "DECIMAL",        "LOWERHEX"),
     ("LOWER_ALPHAHEX", "PUNCT",          "BASE64"),

     ("LOWER",          "DECIMAL",        "LOWER_ALNUM"),
     ("LOWER",          "PUNCT",          "BASE64"),

     ("DECIMAL",        "PUNCT",          "BASE64"),

     # Combinations you can only get after the second symbol
     ("UPPERHEX",       "UPPER_ALPHAHEX", "UPPERHEX"),
     ("UPPERHEX",       "UPPER",          "UPPER_ALNUM"),
     ("UPPERHEX",       "LOWER_ALPHAHEX", "HEX"),
     ("UPPERHEX",       "LOWER",          "ALNUM"),
     ("UPPERHEX",       "DECIMAL",        "UPPERHEX"),
     ("UPPERHEX",       "PUNCT",          "BASE64"),

     ("LOWERHEX",       "UPPER_ALPHAHEX", "HEX"),
     ("LOWERHEX",       "UPPER",          "ALNUM"),
     ("LOWERHEX",       "LOWER_ALPHAHEX", "LOWERHEX"),
     ("LOWERHEX",       "LOWER",          "LOWER_ALNUM"),
     ("LOWERHEX",       "DECIMAL",        "LOWERHEX"),
     ("LOWERHEX",       "PUNCT",          "BASE64"),

     ("ALPHAHEX",       "UPPER_ALPHAHEX", "ALPHAHEX"),
     ("ALPHAHEX",       "UPPER",          "ALPHA"),
     ("ALPHAHEX",       "LOWER_ALPHAHEX", "ALPHAHEX"),
     ("ALPHAHEX",       "LOWER",          "ALPHA"),
     ("ALPHAHEX",       "DECIMAL",        "HEX"),
     ("ALPHAHEX",       "PUNCT",          "BASE64"),

     ("ALPHA",          "UPPER_ALPHAHEX", "ALPHA"),
     ("ALPHA",          "UPPER",          "ALPHA"),
     ("ALPHA",          "LOWER_ALPHAHEX", "ALPHA"),
     ("ALPHA",          "LOWER",          "ALPHA"),
     ("ALPHA",          "DECIMAL",        "ALNUM"),
     ("ALPHA",          "PUNCT",          "BASE64"),

     ("UPPER_ALNUM",    "UPPER_ALPHAHEX", "UPPER_ALNUM"),
     ("UPPER_ALNUM",    "UPPER",          "UPPER_ALNUM"),
     ("UPPER_ALNUM",    "LOWER_ALPHAHEX", "ALNUM"),
     ("UPPER_ALNUM",    "LOWER",          "ALNUM"),
     ("UPPER_ALNUM",    "DECIMAL",        "UPPER_ALNUM"),
     ("UPPER_ALNUM",    "PUNCT",          "BASE64"),

     ("LOWER_ALNUM",    "UPPER_ALPHAHEX", "ALNUM"),
     ("LOWER_ALNUM",    "UPPER",          "ALNUM"),
     ("LOWER_ALNUM",    "LOWER_ALPHAHEX", "LOWER_ALNUM"),
     ("LOWER_ALNUM",    "LOWER",          "LOWER_ALNUM"),
     ("LOWER_ALNUM",    "DECIMAL",        "LOWER_ALNUM"),
     ("LOWER_ALNUM",    "PUNCT",          "BASE64"),

     # Combinations you can only get after the third symbol
     ("HEX",            "UPPER_ALPHAHEX", "HEX"),
     ("HEX",            "UPPER",          "ALNUM"),
     ("HEX",            "LOWER_ALPHAHEX", "HEX"),
     ("HEX",            "LOWER",          "ALNUM"),
     ("HEX",            "DECIMAL",        "HEX"),
     ("HEX",            "PUNCT",          "BASE64"),

     ("ALNUM",          "UPPER_ALPHAHEX", "ALNUM"),
     ("ALNUM",          "UPPER",          "ALNUM"),
     ("ALNUM",          "LOWER_ALPHAHEX", "ALNUM"),
     ("ALNUM",          "LOWER",          "ALNUM"),
     ("ALNUM",          "DECIMAL",        "ALNUM"),
     ("ALNUM",          "PUNCT",          "BASE64"),
     ))
def test_combination(a, b, expect_result):
    """Ensure character type constants combine as they should.
    """
    a, b, expect_result = [
        getattr(_vec64, f"_RT_{ctype}")
        for ctype in (a, b, expect_result)
    ]
    assert (a & b) == expect_result
