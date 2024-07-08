from collections.abc import Iterable


def pair_decode(pairs: Iterable[int]) -> bytes:
    """The inverse of `pair_encode()`.
    """
    return b"".join(
        (b"@@"
         if pair == 4160
         else bytes((pair & 63, pair >> 6)))
        for pair in pairs)
