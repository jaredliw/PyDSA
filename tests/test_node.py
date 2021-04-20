from pydsa.data_structures import Node, NodeType
from tests import is_error


def test_init():
    a = Node(20)
    b = Node(10, next_node=a)

    assert b.next_node == a  # noqa


def test_del():
    a = Node(10, next_node=None)

    def _test():
        del a.value

    is_error(TypeError, _test)

    def _test2():
        del a.next_node  # noqa

    is_error(TypeError, _test2)


def test_get():
    a = Node(10, next_node=None)
    assert a.value == 10

    assert a.next_node is None  # noqa
    is_error(AttributeError, lambda: a.smth_else)  # noqa


def test_repr_str():
    a = Node("Test")
    assert str(a) == "Test"
    assert repr(a) == "Node('Test')"

    b = Node(1)
    assert str(b) == "1"
    assert repr(b) == "Node(1)"


def test_set():
    a = Node()
    b = Node(20, next_node=None)
    b.value = 30
    assert b.value == 30

    b.next_node = a


def test_set_annotations():
    b = Node(70, next_node=None)
    a = Node(70, next_node=b, smth_int=10)
    a.set_annotations(next_node=[None, NodeType], smth_int=int)  # noqa
    b.set_annotations(next_node=[None, NodeType])  # noqa

    a.next_node = b
    assert a.next_node == b

    def _test():
        b.next_node = 123

    is_error(TypeError, _test)

    def _test2():
        a.something_float = 1.2

    is_error(TypeError, _test2)
