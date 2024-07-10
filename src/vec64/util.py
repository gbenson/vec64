from collections.abc import Iterable


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="


def unvectorize(s: bytes) -> str:
    """The inverse function of `vectorize()`.
    """
    return "".join(ALPHABET[c] for c in s)


def pair_decode(pairs: Iterable[int]) -> bytes:
    """The inverse function of `pair_encode()`.
    """
    return b"".join(
        (b"@@"
         if pair == 4160
         else bytes((pair & 63, pair >> 6)))
        for pair in pairs)
