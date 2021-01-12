from pydsa.data_structures.array import ConstantError, DynamicArray, ExceedMaxLengthError, List, StaticArray
from tests import is_error

ds = [StaticArray, DynamicArray]


def test_init():
    for array in ds:
        array([])
        array([1, 2, 3])
        is_error(TypeError, array, 123)
        is_error(TypeError, array, [], 1.2)

    StaticArray([7, 8, 9], 10)
    is_error(ExceedMaxLengthError, StaticArray, [1, 2, 3], 1)


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

    assert StaticArray([1, 2, 3], 6) + StaticArray([4, 5, 6], 5) == StaticArray([1, 2, 3, 4, 5, 6], 7)


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

    assert len(StaticArray([], 10)) == 0


def test_repr_str():
    arr = [1, "Test", set(), [], {1: "10"}, 3.2]
    for array in ds:
        a = array(arr)
        assert str(a) == "[1, 'Test', set(), [], {1: '10'}, 3.2]"

    assert repr(StaticArray(arr)) == "StaticArray([1, 'Test', set(), [], {1: '10'}, 3.2], 6)"
    assert repr(DynamicArray(arr)) == "DynamicArray([1, 'Test', set(), [], {1: '10'}, 3.2], 6)"


def test_reversed():
    a = StaticArray([1, "Test", set(), [], {1: "10"}, 3.2])
    assert repr(StaticArray(reversed(a))) == "StaticArray([3.2, {1: '10'}, [], set(), 'Test', 1], 6)"

    a = DynamicArray([1, "Test", set(), [], {1: "10"}, 3.2])
    assert repr(DynamicArray(reversed(a))) == "DynamicArray([3.2, {1: '10'}, [], set(), 'Test', 1], 6)"


def test_set():
    for array in ds:
        a = array([1, 2, 0.3])
        a.some_random_stuff = 1

    def _test():
        StaticArray([1, 2, 3]).max_length = 10

    is_error(ConstantError, _test)


def test_append():
    a = StaticArray()

    def _test():
        a.append(10)

    is_error(ExceedMaxLengthError, _test)

    b = StaticArray([1, 2, 3], 5)
    b.append(9)
    assert b == StaticArray([1, 2, 3, 9])

    c = DynamicArray([])
    c.append(10)
    assert c == DynamicArray([10])
    assert c.max_length == 1
    assert c != StaticArray([10])
    c.append(20)
    c.append(30)
    assert c == DynamicArray([10, 20, 30])
    assert c.max_length == 4
    c.append(40)
    c.append(50)
    assert c == DynamicArray([10, 20, 30, 40, 50])
    assert c.max_length == 8


def test_clear():
    a = StaticArray([1, 2, 3, 4, 5])
    a.clear()
    assert a == StaticArray([])
    assert a.max_length == 5

    b = DynamicArray([1, 2, 3, 4, 5])
    b.clear()
    assert b == DynamicArray([])
    assert b.max_length == 0


def test_copy():
    a = StaticArray([1], 10)
    b = a.copy()
    assert a == b
    assert a is not b
    b.append(2)
    assert b == StaticArray([1, 2])
    assert a == StaticArray([1])

    c = DynamicArray([1])
    d = c.copy()

    assert c == d
    assert c is not d
    d.append(2)
    assert d == DynamicArray([1, 2])
    assert c == DynamicArray([1])


def test_count():
    for array in ds:
        a = array([])
        assert a.count(0) == 0

        b = array([1, 1, 2, 1, 1, 2, 3])
        assert b.count(1) == 4
        assert b.count(2) == 2
        assert b.count(3) == 1


def test_extend():
    a = StaticArray()
    is_error(ExceedMaxLengthError, a.extend, ["nothing here"])

    b = StaticArray([1, 2, 3], 10)
    b.extend([4, 5, 4, 3, 2])
    assert b == StaticArray([1, 2, 3, 4, 5, 4, 3, 2])
    is_error(ExceedMaxLengthError, b.extend, [0, 0, "exceed"])

    c = DynamicArray([])
    c.extend([1])
    assert c == DynamicArray([1])
    assert c.max_length == 1

    d = DynamicArray([1, 2])
    d.extend(reversed(d))
    d.extend([3, 4, 5, 6, 7, 8, 9])
    assert d == DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
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
    a = StaticArray(max_length=10)
    a.insert(0, 10)
    assert a == StaticArray([10])
    a.insert(-1, 20)
    assert a == StaticArray([20, 10])
    a.insert(1, 15)
    assert a == StaticArray([20, 15, 10])

    b = DynamicArray()
    b.insert(0, 10)
    assert b == DynamicArray([10])
    assert b.max_length == 1
    b.insert(-1, 20)
    assert b == DynamicArray([20, 10])
    assert b.max_length == 2
    b.insert(1, 15)
    assert b == DynamicArray([20, 15, 10])
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

    c = DynamicArray([1, 2, 3, 3, 3, 3, 3, 3])
    for _ in range(6):
        c.remove(3)
    assert c == DynamicArray([1, 2])
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


def test_rotate():
    a = List([])
    a.rotate(5)
    assert a == []

    b = List([1])
    b.rotate(2)
    assert b == [1]

    c = List([1, 2, 3])
    c.rotate(0)
    assert c == [1, 2, 3]
    c.rotate(2)
    assert c == [3, 1, 2]
    c.rotate(81)
    assert c == [3, 1, 2]
    c.rotate(-2)
    assert c == [1, 2, 3]

    is_error(TypeError, c.rotate)
