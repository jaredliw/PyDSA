import math
import random
from inspect import getmembers, isfunction

from pydsa.algorithms import sorting

functs = [member[1] for member in getmembers(sorting) if isfunction(member[1])]
functs.remove(sorting.deepcopy)
functs.remove(sorting.IntList)
functs.remove(sorting.Function)
functs.remove(sorting.NonNegativeInt)
functs.remove(sorting.validate_args)
functs.remove(sorting.is_sorted)
functs.remove(sorting.sleep_sort)
functs.remove(sorting.int_counting_sort)
functs.remove(sorting.radix_sort)


def _test(tc, key=lambda x: x):
    sl = sorted(tc, key=key)
    for f in functs:
        if f in [sorting.bogosort, sorting.bogobogosort, sorting.bozosort, sorting.slowsort, sorting.worstsort]:
            assert f(tc[:5], key=key) == sorted(tc[:5], key=key), f.__name__
            assert f(tc[:5], key=key, reverse=True) == sorted(tc[:5], reverse=True, key=key), f.__name__
        elif f in [sorting.int_counting_sort, sorting.counting_sort]:
            assert f(tc) == sl, f.__name__
            assert f(tc) == sl, f.__name__
        else:
            assert f(tc, key=key) == sl, f.__name__
            assert f(tc, key=key, reverse=True) == sl[::-1], f.__name__


def test_do_modify_original():
    for f in functs + [sorting.sleep_sort, sorting.int_counting_sort]:
        tc = [4, 3, 2, 1]
        f(tc)
        assert tc == [4, 3, 2, 1], f.__name__


def test_empty():
    _test([])


def test_single_item():
    _test([1])


def test_key_funct():
    tc = "This is a test string AA".split()
    functs.append(sorting.counting_sort)
    try:
        _test(tc, key=str.lower)
    finally:
        functs.remove(sorting.counting_sort)


def test_random_integers():
    for _ in range(50):
        tc = [random.randint(-1000, 1000) for _ in range(200)]
        functs.append(sorting.int_counting_sort)
        functs.append(sorting.radix_sort)
        try:
            _test(tc)
        finally:
            functs.remove(sorting.int_counting_sort)
            functs.remove(sorting.radix_sort)


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
