from random import choice, randint, uniform
from inspect import getmembers, isfunction
from pydsa.algorithms import searching

functs = [member[1] for member in getmembers(searching) if isfunction(member[1])]
functs.remove(searching.is_sorted)

def _test(arr, t):
    arr.sort()
    for f in functs:
        print(f)
        idx = f(arr, t)
        if idx == -1:
            assert t not in arr, f.__name__
        else:
            assert arr[idx] == t, f.__name__


def test_empty():
    _test([], 10)


def test_one_element():
    _test([1], -1)
    _test([1], 1)


def test_random_numbers():
    for _ in range(50):
        arr = [choice([uniform(0, 1000), randint(0, 1000)]) for _ in range(100)]
        t = choice(arr)
        _test(arr, t)
        _test(arr, 1001)


def test_chars():
    for _ in range(50):
        arr = list("`1234567890-=~!@#$%^&*()_+qwertyuiop[]QWERTYUIOP{}asdfghjkl;'\\ASDFGHJKL:\"|zxcvbnm,./ZXCVBNM<>?")
        t = choice(arr)
        _test(arr, t)


def test_lists():
    for _ in range(50):
        arr = [[randint(0, 1000) for _ in range(randint(0, 10))] for _ in range(100)]
        t = choice(arr)
        _test(arr, t)
        _test(arr, [-1, -1])
