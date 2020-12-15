import math
import random
import sys
from copy import deepcopy
from inspect import getmembers, isfunction

sys.path.append(".")
sys.path.append("..")
from pydsa.algorithms import sorting

functs = [member[1] for member in getmembers(sorting) if isfunction(member[1])]
functs.remove(sorting.is_sorted)
functs.remove(sorting.sleep_sort)


def _test(inp, key=lambda x: x):
    sl = sorted(deepcopy(inp), key=key)
    for f in functs:
        if f in [sorting.bogosort, sorting.bogobogosort, sorting.bozosort, sorting.slowsort, sorting.worstsort]:
            tc = deepcopy(inp)
            assert f(tc[:5], key=key) == sorted(tc[:5], key=key), f.__name__
            tc = deepcopy(inp)
            assert f(tc[:5], key=key, reverse=True) == sorted(tc[:5], reverse=True, key=key), f.__name__
        else:
            tc = deepcopy(inp)
            assert f(tc, key=key) == sl, f.__name__
            tc = deepcopy(inp)
            assert f(tc, key=key, reverse=True) == sl[::-1], f.__name__


def test_empty():
    for f in functs:
        _test([])


def test_single_item():
    for f in functs:
        _test([1])


def test_key_funct():
    tc = "This is a test string AA".split()
    _test(tc, key=str.lower)


def test_random_integers():
    for _ in range(50):
        tc = [random.randint(-1000, 1000) for _ in range(200)]
        sl = sorted(tc)
        _test(tc)


def test_random_floats():
    for _ in range(50):
        tc = [random.random() for _ in range(200)]
        tc.extend([math.e, math.pi, math.tau, math.sqrt(2), math.sqrt(3)])
        _test(tc)


def test_random_real_numbers():
    for _ in range(50):
        tc = [random.choice([random.random(), random.randint(-1000, 1000)]) for _ in range(200)]
        tc.extend([math.e, math.pi, math.tau, math.sqrt(2), math.sqrt(3)])
        _test(tc)


def test_chars():
    tc = list("`1234567890-=~!@#$%^&*()_+qwertyuiop[]QWERTYUIOP{}asdfghjkl;'\\ASDFGHJKL:\"|zxcvbnm,./ZXCVBNM<>?")
    tc *= 2
    _test(tc)
