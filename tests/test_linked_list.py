from pydsa.data_structures import Node
from pydsa.data_structures.linked_list import *
from tests import is_error

to_test = [SinglyLinkedList, DoublyLinkedList]


def _check(a, ll, ds):
    for idx in range(len(a)):
        cur_node = ll.traverse(idx)
        assert a[idx] == cur_node
        if ds == DoublyLinkedList:
            if idx == 0:
                assert cur_node.last_node is None
            else:
                assert a[idx - 1] == cur_node.last_node
        if idx == len(a) - 1:
            assert cur_node.next_node is None
        else:
            assert a[idx + 1] == cur_node.next_node


def test_init():
    for ds in to_test:
        a = ds([10, 30, 40, None])
        assert a.head == 10
        assert a.head.next_node == 30
        assert a.traverse(-1) == Node(next_node=None)

        a = ds([20])
        assert a.head == 20
        assert a.head.next_node is None

        b = ds("anything")
        assert b.head == "a"

        c = ds([])
        assert c.head is None


def test_op():
    for ds in to_test:
        a = ds([1, 2, 3])
        b = ds([4, 5, 6])
        c = a + b
        assert c == ds([1, 2, 3, 4, 5, 6])
        a.head.next_node.value = 100
        assert c.head.next_node.value == 2
        assert a.head is not c.head

        a = ds([7, 8, 9])
        a += ds([10, 11, "Test"])
        a += ds()
        assert a == ds([7, 8, 9, 10, 11, "Test"])

        c = ds()
        c += ds([7, 8, 9])
        assert c == ds([7, 8, 9])

        assert ds([1, 3, 5]) * 3 == ds([1, 3, 5, 1, 3, 5, 1, 3, 5])
        assert 4 * ds([1, 3, 5]) == ds([1, 3, 5, 1, 3, 5, 1, 3, 5, 1, 3, 5])
        assert ds() * 10 == ds()
        assert ds([1, 3, 5]) * 0 == ds()

        a = ds([2, 4, "a"])
        a *= 2
        assert a == ds([2, 4, "a", 2, 4, "a"])


def test_in():
    for ds in to_test:
        a = ds([1, 0.4, [1, 3], [], "1"])
        assert 1 in a
        assert 2 not in a
        assert [1, 3] in a
        assert [] in a
        assert [1] not in a
        assert "1" in a


def test_compare():
    for ds in to_test:
        assert ds([1, 2, 3]) == ds([1, 2, 3])
        assert ds([]) != ds([1])
        assert ds([1, 2]) < ds([3])
        assert ds([1, 2]) <= ds([3])
        assert ds([]) >= ds([])
        assert ds([4, 4, 4]) >= ds([4, 4])
        assert not ds([1, 2, 3]) > ds([1, 2, 3])
        assert not ds([1, 2, 3]) < ds([1, 2, 3])
        assert ds([]) != []
    assert SinglyLinkedList([1, 2, 3]) != DoublyLinkedList([1, 2, 3])


def test_del():
    for ds in to_test:
        a = ds([1, 2, 3])
        del a.head
        assert a == ds([])

        def _test():
            del a.copy

        is_error(AttributeError, _test)


def test_iter():
    for ds in to_test:
        arr = [4, 3, 2, 5, 5, 4, 3]
        a = ds(arr)
        for idx, item in enumerate(a):
            assert item == arr[idx]

        b = ds([])
        for _ in b:
            assert False


def test_len():
    for ds in to_test:
        assert len(ds([])) == 0
        assert len(ds([1])) == 1
        assert len(ds([[], 10, 3.2, "a"])) == 4


def test_repr_str():
    for ds in to_test:
        a = ds()
        assert repr(a) == "{}()".format(ds.__name__)
        assert str(a) == "{}([])".format(ds.__name__)

        b = ds([1, 2, 3, "10"])
        assert repr(b) == "{}(1 -> 2 -> 3 -> '10')".format(ds.__name__)
        assert str(b) == "{}([1, 2, 3, '10'])".format(ds.__name__)

        circular = ds([1, 2, 3])
        circular.head.next_node.next_node.next_node = circular.head.next_node
        assert repr(circular) == str(circular) == "{}(<cannot show node(s)>)".format(ds.__name__)


def test_reversed():
    for ds in to_test:
        a = [1, "Test", set(), [], {1: "10"}, 3.2]
        ll = ds(a)
        assert reversed(ll) == ds(reversed(a))
        assert reversed(reversed(ll)) == ds(a)  # noqa

        b = ds([])
        assert reversed(b) == ds([])


def test_set():
    for ds in to_test:
        a = ds([1, 2, 0.3])
        a.head = Node(10, next_node=Node(20, next_node=Node(30, next_node=None)))

        assert a.head == 10
        assert a.traverse(2) == 30

        def _test():
            a.some_random_stuff = 1

        is_error(AttributeError, _test)

        a.MAX_ITER = 10
        a.head = Node()


def test_append():
    for ds in to_test:
        a = [1, 3.2, "hello", None, None]
        ll = ds(a)
        a.append(None)
        ll.append(None)
        _check(a, ll, ds)

        if ds == DoublyLinkedList:
            node = ll.traverse(-1)
            idx = -1
            while node is not None:
                assert a[idx] == node
                idx -= 1
                node = node.last_node
            assert idx == len(a) * -1 - 1

        ll2 = ds()
        ll2.append(10)
        ll2.append(20)
        assert ll2.head == 10
        assert ll2.head.next_node == 20
        assert ll2.head.next_node.next_node is None
        if ds == DoublyLinkedList:
            assert ll2.head.next_node.last_node == ll2.head == 10


def test_clear():
    for ds in to_test:
        a = ds([1, 2, None, 3.4, "Hello", True])
        a.clear()
        assert a.head is None
        assert a == ds()

        b = ds([])
        b.clear()
        assert b.head is None
        assert b == ds()


def test_copy():
    for ds in to_test:
        a = ds([1, 2, None, 3.4, "Hello", True])
        b = a.copy()
        assert a == b
        assert a.head is not b.head
        assert a.head.next_node is not b.head.next_node

        c = ds([])
        d = c.copy()
        assert c == d == ds()
        assert c.head is None and d.head is None


def test_count():
    for ds in to_test:
        a = ["hello", 1, 2, 3, None, 1.3, None, "hello", 10]
        sll = ds(a)
        assert a.count(None) == sll.count(None)
        assert a.count("hello") == sll.count("hello")

        sll1 = ds()
        assert sll1.count(10) == 0


def test_extend():
    for ds in to_test:
        a = ds([1, 2, 3])
        a.extend([])
        assert a == ds([1, 2, 3])
        a.extend([4, 5, 6, "123"])
        assert a == ds([1, 2, 3, 4, 5, 6, "123"])

        b = ds()
        b.extend([])
        assert b == ds()
        b.extend(["a", "b", "c"])
        assert b == ds(["a", "b", "c"])


def test_find_middle():
    for ds in to_test:
        a = ds([1, 2, 3, 4, 5])
        middle = a.find_middle()
        assert middle == 3
        assert middle is a.head.next_node.next_node

        b = ds([1, 2, 10, 3.4, "Hello", True])
        middle = b.find_middle()
        assert middle == 10
        assert middle is b.head.next_node.next_node

        c = ds()
        is_error(IndexError, c.find_middle)


def test_detect_cycle():
    for ds in to_test:
        a = ds([1, 2, 10, None, 3.4, "Hello", True, None])
        assert a.detect_cycle() is None

        b = ds(range(100))
        b.MAX_ITER = 110
        b.traverse(-1).next_node = b.head
        assert b.detect_cycle() is b.head


def test_index():
    for ds in to_test:
        a = ds([1, 2, 10, None, 3.4, "Hello", True, None])
        assert a.index(None) == 3
        assert a.index(10) == 2
        assert a.index(True) == 0  # 1 == True
        assert a.index(1) == 0
        assert a.index(3.4, 2, 6) == 4
        assert a.index(3.4, 2, 100) == 4
        assert a.index(3.4, -7, -2) == 4
        assert a.index(3.4, -100, -2) == 4
        assert a.index(None, 1, -3) == 3
        is_error(ValueError, lambda: a.index(1, -1, 0))
        is_error(ValueError, lambda: a.index(2, 5, 0))
        is_error(ValueError, lambda: a.index(2, -10))
        is_error(ValueError, lambda: a.index(3))

        b = ds()
        is_error(ValueError, lambda: b.index(None))
        is_error(ValueError, lambda: b.index(100))

        c = ds([1, 2, 3, 4, 5, 1, 10])
        assert c.index(1, -4) == 5


def test_insert():
    for ds in to_test:
        a = ds()

        a.insert(-1, 10)
        assert a.head == 10
        assert a == ds([10])

        a.insert(0, 1)
        assert a.head == 1
        assert a == ds([1, 10])

        a.insert(1, 5)
        assert a == ds([1, 5, 10])

        a.insert(-2, 3)
        assert a == ds([1, 3, 5, 10])

        a.insert(-4, -10)
        assert a == ds([-10, 1, 3, 5, 10])

        a.insert(100, None)
        assert a == ds([-10, 1, 3, 5, 10, None])

        a.insert(-100, "hello")
        assert a == ds(["hello", -10, 1, 3, 5, 10, None])

        b = ds([1, 2, 10, None, 3.4, "Hello", True, None])
        b.insert(0, None)
        assert b == ds([None, 1, 2, 10, None, 3.4, "Hello", True, None])


def test_pop():
    for ds in to_test:
        a = ds([1, 2, 10, None, 3.4, "Hello", True, None])

        a.pop()
        assert a == ds([1, 2, 10, None, 3.4, "Hello", True])

        a.pop(3)
        assert a == ds([1, 2, 10, 3.4, "Hello", True])

        a.pop(0)
        assert a == ds([2, 10, 3.4, "Hello", True])
        assert a.head == 2

        a.pop(-2)
        assert a == ds([2, 10, 3.4, True])

        a.pop(-4)
        assert a == ds([10, 3.4, True])
        assert a.head == 10

        is_error(IndexError, lambda: ds().pop())
        is_error(IndexError, lambda: ds([""]).pop(1))
        is_error(IndexError, lambda: ds([""]).pop(-2))


def test_remove():
    for ds in to_test:
        a = ds([1, 2, 10, None, 3.4, "Hello", True, None])

        a.remove(None)
        assert a == ds([1, 2, 10, 3.4, "Hello", True, None])

        a.remove(None)
        assert a == ds([1, 2, 10, 3.4, "Hello", True])

        a.remove(1)
        assert a.head == 2
        assert a == ds([2, 10, 3.4, "Hello", True])

        a.remove(True)
        assert a == ds([2, 10, 3.4, "Hello"])

        is_error(ValueError, lambda: a.remove(1011))
        is_error(ValueError, lambda: ds().remove(10))


def test_remove_duplicates():
    for ds in to_test:
        a = ds([1, 2, 10, None, 3.4, "Hello", True])

        a.remove_duplicates()
        assert a == ds([1, 2, 10, None, 3.4, "Hello"])  # True is considered duplicated as there is 1 there

        b = ds([2, 1, 1, 2])
        b.remove_duplicates()
        assert b == ds([2, 1])

        c = ds([2, 1, 1, 1, 1, 1, 1, 3])
        c.remove_duplicates()
        assert c == ds([2, 1, 3])

        d = ds([1, 1, 1, 1, 1, 1])
        d.remove_duplicates()
        assert d == ds([1])

        e = ds([])
        e.remove_duplicates()
        assert e == ds([])

        f = ds([1, 1, 1, 1, 2])
        f.remove_duplicates()
        assert f == ds([1, 2])

        g = ds([2, 1, 3, 1, 4])
        g.remove_duplicates()
        assert g == ds([2, 1, 3, 4])

        circular = ds([1, 2])
        circular.head.next_node.next_node = circular.head
        is_error(ExceededMaxIter, circular.remove_duplicates)


def test_reverse():
    for ds in to_test:
        a = ds([])
        a.reverse()
        assert a == ds([])

        b = ds([1])
        b.reverse()
        assert b == ds([1])

        c = ds([1, 2])
        c.reverse()
        assert c == ds([2, 1])

        d = ds([1, 2, 3, 4, 5, 6, 7])
        e = reversed(d)
        d.reverse()
        assert d == e

        f = ds([1, 3, 5, 3, 2, 4])
        f.reverse()
        assert f == ds([4, 2, 3, 5, 3, 1])

        g = ds([4, 3, "a", 2, 5, 2.1, 2])
        copied = g.copy()
        g.reverse()
        g.reverse()
        assert g == copied


def test_swap():
    def _op(idx1, idx2):
        ll.swap(idx1, idx2)
        a[idx1], a[idx2] = a[idx2], a[idx1]
        assert ll == ds(a)
        _check(a, ll, ds)

    for ds in to_test:
        a = [1, 2, 10, None, 3.4, "Hello", True, None]
        ll = ds(a)

        _op(1, 2)
        _op(0, 6)
        _op(3, -1)
        _op(0, 7)
        _op(-5, -3)
        _op(-1, -1)

        is_error(IndexError, lambda: ll.swap(-9, 0))
        is_error(IndexError, lambda: ll.swap(0, 8))
        is_error(IndexError, lambda: ll.swap(9, -10))


def test_traverse():
    for ds in to_test:
        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, None]
        ll = ds(a)
        for idx in range(-11, 10):
            assert ll.traverse(idx) == a[idx]

        is_error(TypeError, lambda: ll[-12])
        is_error(IndexError, lambda: ll.traverse(-12))
        is_error(IndexError, lambda: ll.traverse(11))
        is_error(IndexError, lambda: ll.traverse(12))

        ll1 = ds([])
        is_error(IndexError, lambda: ll1.traverse(0))
        is_error(IndexError, lambda: ll1.traverse(-1))
        is_error(IndexError, lambda: ll1.traverse(-2))

        b = [10] * 100
        ll2 = ds(b)
        is_error(ExceededMaxIter, lambda: ll2.traverse(100))
