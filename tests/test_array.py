from pydsa.data_structures.array import ConstantError, ExceedMaxLengthError, StaticArray
from tests import is_error


def test_init():
    StaticArray([1, 2, 3], 10)
    is_error(ExceedMaxLengthError, StaticArray, [1, 2, 3], 1)
    is_error(TypeError, StaticArray, 123)
    is_error(TypeError, StaticArray, [], 1.2)


def test_op():
    assert StaticArray([1, 2, 3], 6) + StaticArray([4, 5, 6], 5) == StaticArray([1, 2, 3, 4, 5, 6], 7)
    a = StaticArray([7, 8, 9])
    a += StaticArray([10, 11, "Test"])
    assert a == StaticArray([7, 8, 9, 10, 11, "Test"])

    assert StaticArray([1, 3, 5]) * 3 == StaticArray([1, 3, 5, 1, 3, 5, 1, 3, 5])
    a = StaticArray([2, 4, "a"])
    a *= 2
    assert a == StaticArray([2, 4, "a", 2, 4, "a"])


def test_in():
    a = StaticArray([1, 0.4, [1, 3], [], "1"])
    assert 1 in a
    assert 2 not in a
    assert [1, 3] in a
    assert [] in a
    assert [1] not in a
    assert "1" in a


def test_compare():
    assert StaticArray([1, 2, 3]) == StaticArray([1, 2, 3], 4)
    assert StaticArray([]) != StaticArray([1])
    assert StaticArray([1, 2]) < StaticArray([3])
    assert StaticArray([1, 2]) <= StaticArray([3])
    assert StaticArray([]) >= StaticArray([])
    assert StaticArray([4, 4, 4]) >= StaticArray([4, 3])


def test_del():
    a = StaticArray([1, 2, 3], 4)
    del a[1]
    assert a == StaticArray([1, 3])

    def _test():
        del a.copy

    def _test2():
        del a.max_length

    is_error(AttributeError, _test)
    is_error(AttributeError, _test2)


def test_get():
    a = StaticArray(["a", "c", "b", "d"])
    assert a[2] == "b"
    assert a[0:4] == ["a", "c", "b", "d"]
    assert a[0::2] == ["a", "b"]
    assert a[5::] == []
    assert a.max_length == 4

    def _test():
        return a[10]

    is_error(IndexError, _test)


def test_iter():
    arr = [4, 3, 2, 5, 5, 4, 3]
    a = StaticArray(arr)
    for idx, item in enumerate(a):
        assert item == arr[idx]


def test_len():
    assert len(StaticArray([], 10)) == 0
    assert len(StaticArray([1])) == 1


def test_repr_str():
    a = StaticArray([1, "Test", set(), [], {1: "10"}, 3.2])
    assert repr(a) == "StaticArray([1, 'Test', set(), [], {1: '10'}, 3.2], 6)"
    assert str(a) == "[1, 'Test', set(), [], {1: '10'}, 3.2]"


def test_reversed():
    a = StaticArray([1, "Test", set(), [], {1: "10"}, 3.2])
    assert repr(StaticArray(reversed(a))) == "StaticArray([3.2, {1: '10'}, [], set(), 'Test', 1], 6)"


def test_set():
    a = StaticArray([1, 2, 0.3])
    a.some_random_stuff = 1

    def _test():
        a.max_length = 10

    is_error(ConstantError, _test)


def test_append():
    a = StaticArray()

    def _test():
        a.append(10)

    is_error(ExceedMaxLengthError, _test)

    b = StaticArray([1, 2, 3], 5)
    b.append(9)
    assert b == StaticArray([1, 2, 3, 9])


def test_clear():
    a = StaticArray([1, 2, 3, 4, 5])
    a.clear()
    assert a == StaticArray([])
    assert a.max_length == 5


def test_copy():
    a = StaticArray([1], 10)
    b = a.copy()

    assert a == b
    assert a is not b
    b.append(2)
    assert b == StaticArray([1, 2])
    assert a == StaticArray([1])


def test_count():
    a = StaticArray([])
    assert a.count(0) == 0

    b = StaticArray([1, 1, 2, 1, 1, 2, 3])
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


def test_index():
    a = StaticArray()
    is_error(ValueError, a.index, "")

    b = StaticArray([1, 2, 2, 2, 2, 3])
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


def test_pop():
    a = StaticArray([20, 18, 15, 10])
    a.pop(0)
    assert a == StaticArray([18, 15, 10])
    a.pop(-1)
    assert a == StaticArray([18, 15])
    a.pop(1)
    assert a == StaticArray([18])
    a.pop()
    assert a == StaticArray([])

    def _test():
        a.pop()

    is_error(IndexError, _test)


def test_remove():
    a = StaticArray([])

    def _test():
        a.remove(10)

    is_error(ValueError, _test)
    b = StaticArray([2, 2, 2, 2])
    b.remove(2)
    assert b == StaticArray([2, 2, 2])


def test_reverse():
    a = StaticArray([])
    a.reverse()
    assert a == StaticArray()

    b = StaticArray([2, 3, 1])
    b.reverse()
    assert b == StaticArray([1, 3, 2])


def test_sort():
    a = StaticArray([4, 5, 2, 3, 2])
    a.sort()
    assert a == StaticArray([2, 2, 3, 4, 5])
    assert a.max_length == 5
