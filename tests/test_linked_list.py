from pydsa.data_structures import Node
from pydsa.data_structures.linked_list import SinglyLinkedList
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
    assert a + b == SinglyLinkedList([1, 2, 3, 4, 5, 6])

    a = SinglyLinkedList([7, 8, 9])
    a += SinglyLinkedList([10, 11, "Test"])
    assert a == SinglyLinkedList([7, 8, 9, 10, 11, "Test"])

    assert SinglyLinkedList([1, 3, 5]) * 3 == SinglyLinkedList([1, 3, 5, 1, 3, 5, 1, 3, 5])
    assert 4 * SinglyLinkedList([1, 3, 5]) == SinglyLinkedList([1, 3, 5, 1, 3, 5, 1, 3, 5, 1, 3, 5])

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
    raise NotImplementedError
    # arr = [1, "Test", set(), [], {1: "10"}, 3.2]
    # for array in ds:
    #     a = array(arr)
    #     assert str(a) == "[1, 'Test', set(), [], {1: '10'}, 3.2]"
    #
    # assert repr(StaticArray(arr)) == "StaticArray([1, 'Test', set(), [], {1: '10'}, 3.2], 6)"
    # assert repr(DynamicArray(arr)) == "DynamicArray([1, 'Test', set(), [], {1: '10'}, 3.2], 6)"
    pass


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
