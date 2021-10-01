from pydsa.data_structures.list import *
from tests import is_error

ds = [StaticList, DynamicList]


def test_init():
    for array in ds:
        array([])
        array([1, 2, 3])
        is_error(TypeError, array, 123)
        is_error(TypeError, array, [], 1.2)

    StaticList([7, 8, 9], 10)
    is_error(ExceedMaxLengthError, StaticList, [1, 2, 3], 1)


def test_op():
    for array in ds:
        assert array([1, 2, 3]) + array([4, 5, 6]) == array([1, 2, 3, 4, 5, 6])
        a = array([7, 8, 9])
        a += array([10, 11, "Test"])
        assert a == array([7, 8, 9, 10, 11, "Test"])

        assert array([1, 3, 5]) * 3 == array([1, 3, 5, 1, 3, 5, 1, 3, 5])
        a = array([2, 4, "a"])
        a *= 2
        assert a == array([2, 4, "a", 2, 4, "a"])

    assert StaticList([1, 2, 3], 6) + StaticList([4, 5, 6], 5) == StaticList([1, 2, 3, 4, 5, 6], 7)


def test_in():
    for array in ds:
        a = array([1, 0.4, [1, 3], [], "1"])
        assert 1 in a
        assert 2 not in a
        assert [1, 3] in a
        assert [] in a
        assert [1] not in a
        assert "1" in a


def test_compare():
    for array in ds:
        assert array([1, 2, 3]) == array([1, 2, 3])
        assert array([]) != array([1])
        assert array([1, 2]) < array([3])
        assert array([1, 2]) <= array([3])
        assert array([]) >= array([])
        assert array([4, 4, 4]) >= array([4, 3])
        assert not array([1, 2, 3]) > array([1, 2, 3])
        assert not array([1, 2, 3]) < array([1, 2, 3])
        assert array([]) != []


def test_del():
    for array in ds:
        a = array([1, 2, 3])
        del a[1]
        assert a == array([1, 3])

        def _test():
            del a.copy

        def _test2():
            del a.max_length

        is_error(AttributeError, _test)
        is_error(AttributeError, _test2)


def test_get():
    for array in ds:
        a = array(["a", "c", "b", "d"])
        assert a[2] == "b"
        assert a[0:4] == ["a", "c", "b", "d"]
        assert a[0::2] == ["a", "b"]
        assert a[5::] == []
        assert a.max_length == 4

        def _test():
            return a[10]

        is_error(IndexError, _test)


def test_iter():
    for array in ds:
        arr = [4, 3, 2, 5, 5, 4, 3]
        a = array(arr)
        for idx, item in enumerate(a):
            assert item == arr[idx]


def test_len():
    for array in ds:
        assert len(array([])) == 0
        assert len(array([1])) == 1

    assert len(StaticList([], 10)) == 0


def test_repr_str():
    arr = [1, "Test", set(), [], {1: "10"}, 3.2]
    for array in ds:
        a = array(arr)
        assert str(a) == "[1, 'Test', set(), [], {1: '10'}, 3.2]"

    assert repr(StaticList(arr)) == "StaticList([1, 'Test', set(), [], {1: '10'}, 3.2], 6)"
    assert repr(DynamicList(arr)) == "DynamicList([1, 'Test', set(), [], {1: '10'}, 3.2], 6)"


def test_reversed():
    a = StaticList([1, "Test", set(), [], {1: "10"}, 3.2])
    assert repr(StaticList(reversed(a))) == "StaticList([3.2, {1: '10'}, [], set(), 'Test', 1], 6)"

    a = DynamicList([1, "Test", set(), [], {1: "10"}, 3.2])
    assert repr(DynamicList(reversed(a))) == "DynamicList([3.2, {1: '10'}, [], set(), 'Test', 1], 6)"  # noqa


def test_set():
    for array in ds:
        array([1, 2, 0.3])

        def _test():
            array([4, 5, 6]).some_random_stuff = 1  # noqa

        is_error(AttributeError, _test)

    def _test1():
        StaticList([1, 2, 3]).max_length = 10

    is_error(ConstantError, _test1)

    def _test2():
        DynamicList([1, 2, 3]).max_length = 10  # noqa

    is_error(AttributeError, _test2)


def test_append():
    a = StaticList()

    def _test():
        a.append(10)

    is_error(ExceedMaxLengthError, _test)

    b = StaticList([1, 2, 3], 5)
    b.append(9)
    assert b == StaticList([1, 2, 3, 9])

    c = DynamicList([])
    c.append(10)
    assert c == DynamicList([10])
    assert c.max_length == 1
    assert c != StaticList([10])
    c.append(20)
    c.append(30)
    assert c == DynamicList([10, 20, 30])
    assert c.max_length == 4
    c.append(40)
    c.append(50)
    assert c == DynamicList([10, 20, 30, 40, 50])
    assert c.max_length == 8


def test_clear():
    a = StaticList([1, 2, 3, 4, 5])
    a.clear()
    assert a == StaticList([])
    assert a.max_length == 5

    b = DynamicList([1, 2, 3, 4, 5])
    b.clear()
    assert b == DynamicList([])
    assert b.max_length == 0


def test_copy():
    a = StaticList([1], 10)
    b = a.copy()
    assert a == b
    assert a is not b
    b.append(2)
    assert b == StaticList([1, 2])
    assert a == StaticList([1])

    c = DynamicList([1])
    d = c.copy()

    assert c == d
    assert c is not d
    d.append(2)
    assert d == DynamicList([1, 2])
    assert c == DynamicList([1])


def test_count():
    for array in ds:
        a = array([])
        assert a.count(0) == 0

        b = array([1, 1, 2, 1, 1, 2, 3])
        assert b.count(1) == 4
        assert b.count(2) == 2
        assert b.count(3) == 1


def test_extend():
    a = StaticList()
    is_error(ExceedMaxLengthError, a.extend, ["nothing here"])

    b = StaticList([1, 2, 3], 10)
    b.extend([4, 5, 4, 3, 2])
    assert b == StaticList([1, 2, 3, 4, 5, 4, 3, 2])
    is_error(ExceedMaxLengthError, b.extend, [0, 0, "exceed"])

    c = DynamicList([])
    c.extend([1])
    assert c == DynamicList([1])
    assert c.max_length == 1

    d = DynamicList([1, 2])
    d.extend(reversed(d))  # noqa
    d.extend([3, 4, 5, 6, 7, 8, 9])
    assert d == DynamicList([1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert d.max_length == 16


def test_index():
    for array in ds:
        a = array()
        is_error(ValueError, a.index, "")

        b = array([1, 2, 2, 2, 2, 3])
        assert b.index(1) == 0
        assert b.index(2) == 1
        assert b.index(3) == 5


def test_insert():
    a = StaticList(max_length=10)
    a.insert(0, 10)
    assert a == StaticList([10])
    a.insert(-1, 20)
    assert a == StaticList([20, 10])
    a.insert(1, 15)
    assert a == StaticList([20, 15, 10])

    b = DynamicList()
    b.insert(0, 10)
    assert b == DynamicList([10])
    assert b.max_length == 1
    b.insert(-1, 20)
    assert b == DynamicList([20, 10])
    assert b.max_length == 2
    b.insert(1, 15)
    assert b == DynamicList([20, 15, 10])
    assert b.max_length == 4


def test_pop():
    for array in ds:
        a = array([20, 18, 15, 10])
        a.pop(0)
        assert a == array([18, 15, 10])
        a.pop(-1)
        assert a == array([18, 15])
        a.pop(1)
        assert a == array([18])
        a.pop()
        assert a == array([])

        def _test():
            a.pop()

        is_error(IndexError, _test)


def test_remove():
    for array in ds:
        a = array([])

        def _test():
            a.remove(10)

        is_error(ValueError, _test)
        b = array([2, 2, 2, 2])
        b.remove(2)
        assert b == array([2, 2, 2])

    c = DynamicList([1, 2, 3, 3, 3, 3, 3, 3])
    for _ in range(6):
        c.remove(3)
    assert c == DynamicList([1, 2])
    assert c.max_length == 2


def test_reverse():
    for array in ds:
        a = array([])
        a.reverse()
        assert a == array()

        b = array([2, 3, 1])
        b.reverse()
        assert b == array([1, 3, 2])


def test_sort():
    for array in ds:
        a = array([4, 5, 2, 3, 2])
        a.sort()
        assert a == array([2, 2, 3, 4, 5])
        assert a.max_length == 5
