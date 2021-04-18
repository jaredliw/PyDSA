"""Algorithms for strings."""
from string import ascii_lowercase

from pydsa import validate_args


@validate_args
def is_pangram(string: str, charset: str = ascii_lowercase) -> bool:
    """Check if a string is a pangram / holoalphabetic (contains all letters at least once). E.g. The quick brown fox
    jumps over the lazy dog."""
    return set(charset) <= set(string.lower())
