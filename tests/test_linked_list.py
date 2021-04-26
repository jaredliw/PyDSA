from pydsa.data_structures import Node
from pydsa.data_structures.linked_list import *
from tests import is_error


def test_init():
    a = SinglyLinkedList([10, 30, 40, None])
    assert a.head == 10
    assert a.head.next_node == 30
    assert a.traverse(-1) == Node(next_node=None)

    a = SinglyLinkedList([20])
    assert a.head == 20
    assert a.head.next_node is None

    b = SinglyLinkedList("aaaaa")  # noqa
    assert b.head == "a"

    c = SinglyLinkedList([])
    assert c.head is None


def test_op():
    a = SinglyLinkedList([1, 2, 3])
    b = SinglyLinkedList([4, 5, 6])
    c = a + b
    assert c == SinglyLinkedList([1, 2, 3, 4, 5, 6])
    a.head.next_node.value = 100
    assert c.head.next_node.value == 2
    assert a.head is not c.head

    a = SinglyLinkedList([7, 8, 9])
    a += SinglyLinkedList([10, 11, "Test"])
    a += SinglyLinkedList()
    assert a == SinglyLinkedList([7, 8, 9, 10, 11, "Test"])

    c = SinglyLinkedList()
    c += SinglyLinkedList([7, 8, 9])
    assert c == SinglyLinkedList([7, 8, 9])

    assert SinglyLinkedList([1, 3, 5]) * 3 == SinglyLinkedList([1, 3, 5, 1, 3, 5, 1, 3, 5])
    assert 4 * SinglyLinkedList([1, 3, 5]) == SinglyLinkedList([1, 3, 5, 1, 3, 5, 1, 3, 5, 1, 3, 5])
    assert SinglyLinkedList() * 10 == SinglyLinkedList()
    assert SinglyLinkedList([1, 3, 5]) * 0 == SinglyLinkedList()

    a = SinglyLinkedList([2, 4, "a"])
    a *= 2
    assert a == SinglyLinkedList([2, 4, "a", 2, 4, "a"])


def test_in():
    a = SinglyLinkedList([1, 0.4, [1, 3], [], "1"])
    assert 1 in a
    assert 2 not in a
    assert [1, 3] in a
    assert [] in a
    assert [1] not in a
    assert "1" in a


def test_compare():
    assert SinglyLinkedList([1, 2, 3]) == SinglyLinkedList([1, 2, 3])
    assert SinglyLinkedList([]) != SinglyLinkedList([1])
    assert SinglyLinkedList([1, 2]) < SinglyLinkedList([3])
    assert SinglyLinkedList([1, 2]) <= SinglyLinkedList([3])
    assert SinglyLinkedList([]) >= SinglyLinkedList([])
    assert SinglyLinkedList([4, 4, 4]) >= SinglyLinkedList([4, 4])
    assert SinglyLinkedList([]) != []


def test_del():
    a = SinglyLinkedList([1, 2, 3])
    del a.head
    assert a == SinglyLinkedList([])

    def _test():
        del a.copy

    is_error(AttributeError, _test)


def test_iter():
    arr = [4, 3, 2, 5, 5, 4, 3]
    a = SinglyLinkedList(arr)
    for idx, item in enumerate(a):
        assert item == arr[idx]

    b = SinglyLinkedList([])
    for item in b:
        assert item is None


def test_len():
    assert len(SinglyLinkedList([])) == 0
    assert len(SinglyLinkedList([1])) == 1
    assert len(SinglyLinkedList([[], 10, 3.2, "a"])) == 4


def test_repr_str():
    a = SinglyLinkedList()
    assert repr(a) == "SinglyLinkedList()"
    assert str(a) == "SinglyLinkedList([])"

    b = SinglyLinkedList([1, 2, 3, "10"])
    print(type(b.head.next_node.next_node.next_node.value))
    assert repr(b) == "SinglyLinkedList(1 -> 2 -> 3 -> '10')"
    assert str(b) == "SinglyLinkedList([1, 2, 3, '10'])"

    circular = SinglyLinkedList([1, 2, 3])
    circular.head.next_node.next_node.next_node = circular.head.next_node
    assert repr(circular) == str(circular) == "SinglyLinkedList(<cannot show node(s)>)"


def test_reversed():
    a = SinglyLinkedList([1, "Test", set(), [], {1: "10"}, 3.2])
    assert reversed(a) == SinglyLinkedList([3.2, {1: '10'}, [], set(), 'Test', 1])

    b = SinglyLinkedList([])
    assert reversed(b) == SinglyLinkedList([])


def test_set():
    a = SinglyLinkedList([1, 2, 0.3])
    a.head = Node(10, next_node=Node(20, next_node=Node(30, next_node=None)))

    assert a.head == 10
    assert a.traverse(2) == 30

    def _test():
        a.some_random_stuff = 1

    is_error(AttributeError, _test)


def test_append():
    a = [1, 3.2, "hello", None, None]
    sll = SinglyLinkedList(a)
    a.append(None)
    sll.append(None)
    for idx in range(len(a)):
        assert a[idx] == sll.traverse(idx)

    sll2 = SinglyLinkedList()
    sll2.append(10)
    sll2.append(20)
    assert sll2.head == 10
    assert sll2.head.next_node == 20


def test_clear():
    a = SinglyLinkedList([1, 2, None, 3.4, "Hello", True])
    a.clear()
    assert a.head is None
    assert a == SinglyLinkedList()

    b = SinglyLinkedList([])
    b.clear()
    assert b.head is None
    assert b == SinglyLinkedList()


def test_copy():
    a = SinglyLinkedList([1, 2, None, 3.4, "Hello", True])
    b = a.copy()
    assert a == b
    assert a.head is not b.head
    assert a.head.next_node is not b.head.next_node

    c = SinglyLinkedList([])
    d = c.copy()
    assert c == d == SinglyLinkedList()
    assert c.head is None and d.head is None


def test_count():
    a = ["hello", 1, 2, 3, None, 1.3, None, "hello", 10]
    sll = SinglyLinkedList(a)
    assert a.count(None) == sll.count(None)
    assert a.count("hello") == sll.count("hello")

    sll1 = SinglyLinkedList()
    assert sll1.count(10) == 0


def test_extend():
    a = SinglyLinkedList([1, 2, 3])
    a.extend([])
    assert a == SinglyLinkedList([1, 2, 3])
    a.extend([4, 5, 6, "123"])
    assert a == SinglyLinkedList([1, 2, 3, 4, 5, 6, "123"])

    b = SinglyLinkedList()
    b.extend([])
    assert b == SinglyLinkedList()
    b.extend(["a", "b", "c"])
    assert b == SinglyLinkedList(["a", "b", "c"])


def test_find_middle():
    a = SinglyLinkedList([1, 2, 3, 4, 5])
    middle = a.find_middle()
    assert middle == 3
    assert middle is a.head.next_node.next_node

    b = SinglyLinkedList([1, 2, 10, 3.4, "Hello", True])
    middle = b.find_middle()
    assert middle == 10
    assert middle is b.head.next_node.next_node

    c = SinglyLinkedList()
    is_error(ValueError, c.find_middle)


def test_detect_cycle():
    a = SinglyLinkedList([1, 2, 10, None, 3.4, "Hello", True, None])
    assert a.detect_cycle() is None

    b = SinglyLinkedList(range(100))
    b.MAX_ITER = 110
    b.traverse(-1).next_node = b.head
    assert b.detect_cycle() is b.head


def test_index():
    a = SinglyLinkedList([1, 2, 10, None, 3.4, "Hello", True, None])
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

    b = SinglyLinkedList()
    is_error(ValueError, lambda: b.index(None))
    is_error(ValueError, lambda: b.index(100))

    c = SinglyLinkedList([1, 2, 3, 4, 5, 1, 10])
    assert c.index(1, -4) == 5

def test_insert():
    a = SinglyLinkedList()

    a.insert(-1, 10)
    assert a.head == 10
    assert a == SinglyLinkedList([10])

    a.insert(0, 1)
    assert a.head == 1
    assert a == SinglyLinkedList([1, 10])

    a.insert(1, 5)
    assert a == SinglyLinkedList([1, 5, 10])

    a.insert(-2, 3)
    assert a == SinglyLinkedList([1, 3, 5, 10])

    a.insert(-4, -10)
    assert a == SinglyLinkedList([-10, 1, 3, 5, 10])

    a.insert(100, None)
    assert a == SinglyLinkedList([-10, 1, 3, 5, 10, None])

    a.insert(-100, "hello")
    assert a == SinglyLinkedList(["hello", -10, 1, 3, 5, 10, None])

    b = SinglyLinkedList([1, 2, 10, None, 3.4, "Hello", True, None])
    b.insert(0, None)
    assert b == SinglyLinkedList([None, 1, 2, 10, None, 3.4, "Hello", True, None])


def test_pop():
    a = SinglyLinkedList([1, 2, 10, None, 3.4, "Hello", True, None])

    a.pop()
    assert a == SinglyLinkedList([1, 2, 10, None, 3.4, "Hello", True])

    a.pop(3)
    assert a == SinglyLinkedList([1, 2, 10, 3.4, "Hello", True])

    a.pop(0)
    assert a == SinglyLinkedList([2, 10, 3.4, "Hello", True])
    assert a.head == 2

    a.pop(-2)
    assert a == SinglyLinkedList([2, 10, 3.4, True])

    a.pop(-4)
    assert a == SinglyLinkedList([10, 3.4, True])
    assert a.head == 10

    is_error(IndexError, lambda: SinglyLinkedList().pop())
    is_error(IndexError, lambda: SinglyLinkedList([""]).pop(1))
    is_error(IndexError, lambda: SinglyLinkedList([""]).pop(-2))


def test_remove():
    a = SinglyLinkedList([1, 2, 10, None, 3.4, "Hello", True, None])

    a.remove(None)
    assert a == SinglyLinkedList([1, 2, 10, 3.4, "Hello", True, None])

    a.remove(None)
    assert a == SinglyLinkedList([1, 2, 10, 3.4, "Hello", True])

    a.remove(1)
    assert a.head == 2
    assert a == SinglyLinkedList([2, 10, 3.4, "Hello", True])

    a.remove(True)
    assert a == SinglyLinkedList([2, 10, 3.4, "Hello"])

    is_error(ValueError, lambda: a.remove(1011))
    is_error(ValueError, lambda: SinglyLinkedList().remove(10))


def test_remove_duplicates():
    a = SinglyLinkedList([1, 2, 10, None, 3.4, "Hello", True])

    a.remove_duplicates()
    assert a == SinglyLinkedList([1, 2, 10, None, 3.4, "Hello"])  # True is considered duplicated as there is 1 there

    b = SinglyLinkedList([2, 1, 1, 2])
    b.remove_duplicates()
    assert b == SinglyLinkedList([2, 1])

    c = SinglyLinkedList([2, 1, 1, 1, 1, 1, 1, 3])
    c.remove_duplicates()
    assert c == SinglyLinkedList([2, 1, 3])

    d = SinglyLinkedList([1, 1, 1, 1, 1, 1])
    d.remove_duplicates()
    assert d == SinglyLinkedList([1])

    e = SinglyLinkedList([])
    e.remove_duplicates()
    assert e == SinglyLinkedList([])

    f = SinglyLinkedList([1, 1, 1, 1, 2])
    f.remove_duplicates()
    assert f == SinglyLinkedList([1, 2])

    g = SinglyLinkedList([2, 1, 3, 1, 4])
    g.remove_duplicates()
    assert g == SinglyLinkedList([2, 1, 3, 4])

    circular = SinglyLinkedList([1, 2])
    circular.head.next_node.next_node = circular.head
    is_error(ExceededMaxIterations, circular.remove_duplicates)


def test_reverse():
    a = SinglyLinkedList([])
    a.reverse()
    assert a == SinglyLinkedList([])

    b = SinglyLinkedList([1])
    b.reverse()
    assert b == SinglyLinkedList([1])

    c = SinglyLinkedList([1, 2])
    c.reverse()
    assert c == SinglyLinkedList([2, 1])

    d = SinglyLinkedList([1, 2, 3, 4, 5, 6, 7])
    e = reversed(d)
    d.reverse()
    assert d == e

    f = SinglyLinkedList([1, 3, 5, 3, 2, 4])
    f.reverse()
    assert f == SinglyLinkedList([4, 2, 3, 5, 3, 1])


def test_swap():
    a = SinglyLinkedList([1, 2, 10, None, 3.4, "Hello", True, None])

    a.swap(1, 2)
    assert a == SinglyLinkedList([1, 10, 2, None, 3.4, "Hello", True, None])

    a.swap(0, 6)
    assert a == SinglyLinkedList([True, 10, 2, None, 3.4, "Hello", 1, None])

    a.swap(3, -1)
    assert a == SinglyLinkedList([True, 10, 2, None, 3.4, "Hello", 1, None])

    a.swap(0, 7)
    assert a == SinglyLinkedList([None, 10, 2, None, 3.4, "Hello", 1, True])

    a.swap(-5, -3)
    assert a == SinglyLinkedList([None, 10, 2, "Hello", 3.4, None, 1, True])

    a.swap(-1, -1)
    assert a == SinglyLinkedList([None, 10, 2, "Hello", 3.4, None, 1, True])

    is_error(IndexError, lambda: a.swap(-9, 0))
    is_error(IndexError, lambda: a.swap(0, 8))
    is_error(IndexError, lambda: a.swap(9, -10))


def test_traverse():
    a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, None]
    sll = SinglyLinkedList(a)
    for idx in range(-11, 10):
        assert sll.traverse(idx) == a[idx]

    is_error(TypeError, lambda: sll[-12])  # noqa, do on purpose
    is_error(IndexError, lambda: sll.traverse(-12))
    is_error(IndexError, lambda: sll.traverse(11))
    is_error(IndexError, lambda: sll.traverse(12))

    sll1 = SinglyLinkedList([])
    is_error(IndexError, lambda: sll1.traverse(0))
    is_error(IndexError, lambda: sll1.traverse(-1))
    is_error(IndexError, lambda: sll1.traverse(-2))

    b = [10] * 100
    sll1 = SinglyLinkedList(b)
    is_error(ExceededMaxIterations, lambda: sll1.traverse(100))
