from pydsa.algorithms.strings import *


def test_is_pangram():
    assert is_pangram("The quick brown fox jumps over the lazy dog 1234!")
    assert not is_pangram("hello world!")
