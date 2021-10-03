from pytest import mark

from pydsa.data_structures.list import *
from tests import is_error

ds = [StaticList, DynamicList]


@mark.parametrize("item", ds)
def test_init(item):
    item([])
    item([1, 2, 3])
    is_error(TypeError, item, 123)
    is_error(TypeError, item, [], 1.2)

    if item == StaticList:
        item([7, 8, 9], 10)
        is_error(ExceedMaxLengthError, item, [1, 2, 3], 1)


@mark.parametrize("item", ds)
def test_op_add(item):
    if item == StaticList:
        assert item([1, 2, 3], 6) + item([4, 5, 6]) == item([1, 2, 3, 4, 5, 6])

        def _test():
            item([1, 2, 3]) + item([4, 5, 6])

        is_error(ExceedMaxLengthError, _test)

        def _test1():
            item([1, 2, 3]) + item([4, 5, 6], 100)

        is_error(ExceedMaxLengthError, _test1)

        a = item([7, 8, 9], 6)
        a += item([10, 11, "Test"])
        assert a == item([7, 8, 9, 10, 11, "Test"])

        def _test2():
            b = item([1, 2, 3])
            b += item([4, 5, 6])

        is_error(ExceedMaxLengthError, _test2)

        def _test3():
            a + [1, 2, 3]

        is_error(TypeError, _test3)

        def _test4():
            a + DynamicList([1, 2, 3])

        is_error(TypeError, _test4)
    elif item == DynamicList:
        assert item([1, 2, 3]) + item([4, 5, 6]) == item([1, 2, 3, 4, 5, 6])

        a = item(["a", "b"])
        a += ["c", "d"]
        assert a == item("abcd")


@mark.parametrize("item", ds)
def test_op_mul(item):
    if item == StaticList:
        a = item([7, 8, 9], 12)
    else:
        a = item([7, 8, 9])
    a *= 4
    assert a == item([7, 8, 9, 7, 8, 9, 7, 8, 9, 7, 8, 9])
    a *= 1
    assert a == item([7, 8, 9, 7, 8, 9, 7, 8, 9, 7, 8, 9])
    a *= 0
    assert a == item([])
    a *= -1
    assert a == item([])
    a *= -100
    assert a == item([])
    assert isinstance(a, item)

    assert 4 * item([7, 8, 9], 12) == item([7, 8, 9, 7, 8, 9, 7, 8, 9, 7, 8, 9])
    assert item([7, 8, 9]) * 1 == item([7, 8, 9])
    assert item([7, 8, 9]) * 0 == item([])
    assert item([7, 8, 9]) * -1 == item([])
    assert -100 * item([7, 8, 9]) == item([])
    assert isinstance(3 * item([7, 8, 9], 12), item)

    if item == StaticList:
        def _test():
            item([1, 2, 3]) * 3

        is_error(ExceedMaxLengthError, _test)


@mark.parametrize("item", ds)
def test_in(item):
    a = item([1, 0.4, [1, 3], [], "1"])
    assert 1 in a
    assert 2 not in a
    assert [1, 3] in a
    assert [] in a
    assert [1] not in a
    assert "1" in a


@mark.parametrize("item", ds)
def test_compare(item):
    assert item([1, 2, 3]) == item([1, 2, 3])
    assert item([]) != item([1])
    assert item([1, 2]) < item([3])
    assert item([1, 2]) <= item([3])
    assert item([]) >= item([])
    assert item([4, 4, 4]) >= item([4, 3])
    assert not item([1, 2, 3]) > item([1, 2, 3])
    assert not item([1, 2, 3]) < item([1, 2, 3])
    assert item([]) != []


@mark.parametrize("item", ds)
def test_del(item):
    a = item([1, 2, 3])
    del a[1]
    assert a == item([1, 3])

    def _test():
        del a.copy

    is_error(AttributeError, _test)

    def _test1():
        del a.some_random_stuff

    is_error(AttributeError, _test1)

    def _test2():
        del a.max_length

    is_error(AttributeError, _test2)


@mark.parametrize("item", ds)
def test_get(item):
    a = item(["a", "c", "b", "d"])
    assert a[2] == "b"
    assert a[0:4] == ["a", "c", "b", "d"]
    assert a[0::2] == ["a", "b"]
    assert a[5::] == []
    assert a.max_length == 4

    def _test():
        return a[10]

    is_error(IndexError, _test)


@mark.parametrize("item", ds)
def test_iter(item):
    arr = [4, 3, 2, 5, 5, 4, 3]
    a = item(arr)
    for ori, item in zip(arr, a):
        assert ori == item


@mark.parametrize("item", ds)
def test_len(item):
    assert len(item([])) == 0
    assert len(item([1])) == 1

    if item == StaticList:
        assert len(item([], 10)) == 0


@mark.parametrize("item", ds)
def test_repr_str(item):
    arr = [1, "Test", set(), [], {1: "10"}, 3.2]
    a = item(arr)
    assert str(a) == "[1, 'Test', set(), [], {1: '10'}, 3.2]"
    assert repr(item(arr)) == f"{item().__class__.__name__}([1, 'Test', set(), [], {{1: '10'}}, 3.2], 6)"


@mark.parametrize("item", ds)
def test_reversed(item):
    a = item([1, "Test", set(), [], {1: "10"}, 3.2])
    assert repr(item(reversed(a))) == f"{item().__class__.__name__}([3.2, {{1: '10'}}, [], set(), 'Test', 1], 6)"


@mark.parametrize("item", ds)
def test_set(item):
    item([1, 2, 0.3])

    def _test():
        item([4, 5, 6]).some_random_stuff = 1  # noqa

    is_error(AttributeError, _test)

    def _test1():
        item([1, 2, 3]).max_length = 10

    is_error(ConstantError, _test1)


@mark.parametrize("item", ds)
def test_append(item):
    if item == StaticList:
        a = item()

        def _test():
            a.append(10)

        is_error(ExceedMaxLengthError, _test)

        b = item([1, 2, 3], 5)
        b.append(9)
        assert b == item([1, 2, 3, 9])
    elif item == DynamicList:
        c = item([])
        c.append(10)
        assert c == item([10])
        assert c.max_length == 1
        assert c != StaticList([10])
        c.append(20)
        c.append(30)
        assert c == item([10, 20, 30])
        assert c.max_length == 4
        c.append(40)
        c.append(50)
        assert c == item([10, 20, 30, 40, 50])
        assert c.max_length == 8


@mark.parametrize("item", ds)
def test_clear(item):
    a = item([1, 2, 3, 4, 5])
    a.clear()
    assert a == item([])
    if item == StaticList:
        assert a.max_length == 5
    elif item == DynamicList:
        assert a.max_length == 0


@mark.parametrize("item", ds)
def test_copy(item):
    if item == StaticList:
        a = item([1], max_length=2)
    else:
        a = item([1])
    b = a.copy()
    assert a == b
    assert a is not b
    b.append(2)
    assert b == item([1, 2])
    assert a == item([1])


@mark.parametrize("item", ds)
def test_count(item):
    a = item([])
    assert a.count(0) == 0

    b = item([1, 1, 2, 1, 1, 2, 3])
    assert b.count(1) == 4
    assert b.count(2) == 2
    assert b.count(3) == 1


@mark.parametrize("item", ds)
def test_extend(item):
    if item == StaticList:
        a = item()
        is_error(ExceedMaxLengthError, a.extend, ["nothing here"])

        b = item([1, 2, 3], 10)
        b.extend([4, 5, 4, 3, 2])
        assert b == item([1, 2, 3, 4, 5, 4, 3, 2])
        is_error(ExceedMaxLengthError, b.extend, [0, 0, "exceed"])
    elif item == DynamicList:
        c = item([])
        c.extend([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        assert c == item([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        assert c.max_length == 1

        d = item([1, 2])
        d.extend(reversed(d))  # noqa
        d.extend([3, 4, 5, 6, 7, 8, 9])
        assert d == item([1, 2, 3, 4, 5, 6, 7, 8, 9])
        assert d.max_length == 16

    if item == StaticList:
        e = item(max_length=50)
    else:
        e = item()
    e.extend(filter(lambda x: x % 2, range(10)))
    assert e == item([1, 3, 5, 7, 9])


@mark.parametrize("item", ds)
def test_index(item):
    a = item()
    is_error(ValueError, a.index, "")

    b = item([1, 2, 2, 2, 2, 3])
    assert b.index(1) == 0
    assert b.index(2) == 1
    assert b.index(3) == 5


@mark.parametrize("item", ds)
def test_insert(item):
    if item == StaticList:
        a = item(max_length=10)
    else:
        a = item()
    a.insert(0, 10)
    assert a == item([10])
    if item == DynamicList:
        assert a.max_length == 1
    a.insert(-1, 20)
    assert a == item([20, 10])
    if item == DynamicList:
        assert a.max_length == 2
    a.insert(1, 15)
    assert a == item([20, 15, 10])
    if item == DynamicList:
        assert a.max_length == 4


@mark.parametrize("item", ds)
def test_pop(item):
    a = item([20, 18, 15, 10])
    a.pop(0)
    assert a == item([18, 15, 10])
    a.pop(-1)
    assert a == item([18, 15])
    a.pop(1)
    assert a == item([18])
    a.pop()
    assert a == item([])

    def _test():
        a.pop()

    is_error(IndexError, _test)


@mark.parametrize("item", ds)
def test_remove(item):
    a = item([])

    def _test():
        a.remove(10)

    is_error(ValueError, _test)
    b = item([2, 2, 2, 2])
    b.remove(2)
    assert b == item([2, 2, 2])

    if item == DynamicList:
        c = item([1, 2, 3, 3, 3, 3, 3, 3])
        for _ in range(6):
            c.remove(3)
        assert c == item([1, 2])
        assert c.max_length == 2


@mark.parametrize("item", ds)
def test_reverse(item):
    a = item([])
    a.reverse()
    assert a == item()

    b = item([2, 3, 1])
    b.reverse()
    assert b == item([1, 3, 2])


@mark.parametrize("item", ds)
def test_sort(item):
    a = item([4, 5, 2, 3, 2])
    a.sort()
    assert a == item([2, 2, 3, 4, 5])
    assert a.max_length == 5
