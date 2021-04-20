import math
import random

from pydsa.algorithms import sorting

functs = set(sorting.__dict__[f_name] for f_name in sorting.__all__)
functs.remove(sorting.is_sorted)

slow_group = {sorting.bogosort, sorting.bogobogosort, sorting.bozosort, sorting.slowsort, sorting.worstsort,
              sorting.sleep_sort}
no_key_group = {sorting.counting_sort}


def _test(tc, key=lambda x: x, exclude=None):
    if exclude is None:
        exclude = {}

    sl = sorted(tc, key=key)
    for f in functs:
        if f in exclude:
            continue
        elif f in slow_group:
            assert f(tc[:5], key=key) == sorted(tc[:5], key=key), f.__name__
            assert f(tc[:5], key=key, reverse=True) == sorted(tc[:5], reverse=True, key=key), f.__name__
        elif f in no_key_group:
            assert f(tc) == sl, f.__name__
            assert f(tc, reverse=True) == sl[::-1], f.__name__
        else:
            assert f(tc, key=key) == sl, f.__name__
            assert f(tc, key=key, reverse=True) == sl[::-1], f.__name__


def test_do_modify_original():
    for f in functs:
        tc = [4, 3, 2, 1]
        f(tc)
        assert tc == [4, 3, 2, 1], f.__name__


def test_empty():
    _test([])


def test_single_item():
    _test([1])


def test_str_with_key():
    exclude = {sorting.counting_sort, sorting.bucket_sort, sorting.sleep_sort, sorting.pigeonhole_sort,
               sorting.radix_sort, sorting.bead_sort, sorting.proxmap_sort}

    tc = "This is a test string AA".split()
    _test(tc, key=str.lower, exclude=exclude)


def test_random_integers():
    exclude = {sorting.sleep_sort}

    for _ in range(50):
        tc = [random.randint(-10000, 10000) for _ in range(5)]
        _test(tc, exclude=exclude)


def test_random_floats():
    exclude = {sorting.sleep_sort, sorting.pigeonhole_sort, sorting.radix_sort, sorting.bead_sort,
               sorting.counting_sort}

    for _ in range(50):
        tc = [random.random() for _ in range(200)]
        tc.extend([math.e, math.pi, math.tau, math.sqrt(2), math.sqrt(3)])
        _test(tc, exclude=exclude)


def test_random_real_numbers():
    exclude = {sorting.sleep_sort, sorting.pigeonhole_sort, sorting.radix_sort, sorting.bead_sort,
               sorting.counting_sort}

    for _ in range(50):
        tc = [random.choice([random.random(), random.randint(-1000, 1000)]) for _ in range(200)]
        tc.extend([math.e, math.pi, math.tau, math.sqrt(2), math.sqrt(3)])
        _test(tc, exclude=exclude)


def test_chars():
    exclude = {sorting.bucket_sort, sorting.sleep_sort, sorting.pigeonhole_sort, sorting.radix_sort,
               sorting.bead_sort, sorting.counting_sort, sorting.proxmap_sort}

    # noinspection SpellCheckingInspection
    tc = list("`1234567890-=~!@#$%^&*()_+qwertyuiop[]QWERTYUIOP{}asdfghjkl;'\\ASDFGHJKL:\"|zxcvbnm,./ZXCVBNM<>?")
    tc *= 2
    _test(tc, exclude=exclude)


def test_key():
    include = {sorting.bucket_sort, sorting.sleep_sort, sorting.pigeonhole_sort, sorting.radix_sort,
               sorting.bead_sort}

    # noinspection SpellCheckingInspection
    tc = list("`1234567890-=~!@#$%^&*()_+qwertyuiop[]QWERTYUIOP{}asdfghjkl;'\\ASDFGHJKL:\"|zxcvbnm,./ZXCVBNM<>?")
    tc *= 2

    exclude = functs - include
    exclude.update({sorting.bead_sort, sorting.sleep_sort})
    _test(tc, key=ord, exclude=exclude)

    # test bead_sort
    ans = sorted(map(ord, tc))
    assert ans == sorting.bead_sort(tc, key=ord)
    assert ans[::-1] == sorting.bead_sort(tc, key=ord, reverse=True)
