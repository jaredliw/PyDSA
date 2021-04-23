"""A linear data structure where each element is a separate object."""
import sys
from copy import deepcopy

from pydsa import Any, Iterable, validate_args, PositiveInt
from pydsa.data_structures import Node, NodeType

__all__ = ["ExceededMaxIterations", "SinglyLinkedList"]


class ExceededMaxIterations(RuntimeWarning):
    """Raised when maximum iterations has been exceeded."""
    pass


class SinglyLinkedList:
    """A one-way linear data structure where elements are separated and non-contiguous objects that linked by
    pointers. """
    MAX_ITER = 99
    head = None

    @validate_args
    def __init__(self, iterable: Iterable = None):
        if iterable is None:
            self.head = None
        else:
            self.extend(iterable)

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(
                "unsupported operand type(s) for +: '{}' and '{}'".format(type(self).__name__, type(other).__name__))
        new = self.copy()
        new += other
        return new

    def __contains__(self, item):
        try:
            self.index(item)
        except ValueError:
            return False
        else:
            return True

    def __delattr__(self, item):
        if item == "head":
            self.clear()
        else:
            raise AttributeError("'{}' object has no attribute {}".format(type(self).__name__, item))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if len(self) != len(other):
                return False
            for node1, node2 in zip(self, other):
                if node1 != node2:
                    return False
            return True
        return False

    def __ge__(self, other):
        return not self.__lt__(other)

    def __gt__(self, other):
        return (not self.__lt__(other)) and (not self.__eq__(other))

    def __iadd__(self, other):  # todo
        if not isinstance(other, self.__class__):
            raise TypeError(
                "unsupported operand type(s) for +=: '{}' and '{}'".format(type(self).__name__, type(other).__name__))
        copied = other.copy()
        if self.head is None:
            self.head = copied.head
        else:
            node = self.traverse(-1)
            node.next_node = copied.head
        return self

    def __imul__(self, other):
        if not isinstance(other, int):
            raise TypeError(
                "unsupported operand type(s) for *=: '{}' and '{}'".format(type(self).__name__, type(other).__name__))
        if other <= 0:
            self.clear()
        else:
            new = self.copy()
            for _ in range(other - 1):
                self.__iadd__(new)
                new = new.copy()
        return self

    def __iter__(self):
        count = 0
        current = self.head
        while current is not None:
            count += 1
            if count > self.MAX_ITER:
                raise ExceededMaxIterations("maximum number of iteration has been exceeded. Make sure there is no "
                                            "cycle in the linked list by using detect_cycle() or increase "
                                            "MAX_ITER")
            yield current
            current = current.next_node

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __len__(self):
        return sum(1 for _ in self)

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("'<' not supported between instances of '{}' and '{}'".format(type(self).__name__,
                                                                                          type(other).__name__))
        for self_item, other_item in zip(self, other):
            if self_item < other_item:
                return True

        if len(self) < len(other):
            return True
        else:
            return False

    def __mul__(self, other):
        if not isinstance(other, int):
            raise TypeError(
                "unsupported operand type(s) for *: '{}' and '{}'".format(type(self).__name__, type(other).__name__))
        new = self.copy()
        new *= other
        return new

    def __ne__(self, other):
        return not self.__eq__(other)

    def __reversed__(self):
        new_l = self.copy()
        new_l.reverse()
        return new_l

    def __rmul__(self, other):
        return self.__mul__(other)

    def __setattr__(self, key, value):
        if key == "head":
            if isinstance(value, Node) or value is None:
                self.__dict__[key] = value
            else:
                raise ValueError("Value of '{}' should be a(n) '{}', not '{}'"
                                 .format(key, NodeType.__name__, type(value).__name__))
        else:
            raise AttributeError("'{}' object has no attribute {}".format(type(self).__name__, key))

    def __str__(self):
        try:
            to_list = []
            for item in self:
                to_list.append(item.value)
            return "{}({})".format(type(self).__name__, str(to_list))
        except ExceededMaxIterations:
            return "{}({})".format(type(self).__name__, "<cannot show node(s)>")

    def __repr__(self):
        try:
            return "{}({})".format(type(self).__name__, " -> ".join(map(lambda x: repr(x.value), self)))
        except ExceededMaxIterations:
            return "{}({})".format(type(self).__name__, "<cannot show node(s)>")

    @validate_args
    def append(self, value: Any) -> None:
        """Append a new node with value given to the end of the list."""
        # Time Complexity: O(1), but it take O(n) to traverse to the node at the index given

        self.insert(-1, value)

    @validate_args
    def clear(self) -> None:
        """Remove all items from singly linked list,"""
        # Time Complexity: O(1)

        self.head = None

    @validate_args
    def copy(self):
        """Return a deep copy of the linked list."""
        # Time Complexity: O(n)

        return deepcopy(self)

    @validate_args
    def count(self, value):
        """Return number of occurrences of value."""
        # Time Complexity: O(n)

        counter = 0
        for item in self:
            if item == value:
                counter += 1
        return counter

    @validate_args
    def extend(self, iterable: Iterable) -> None:
        """Extend singly linked list by appending elements from the iterable."""
        # Time Complexity: O(n), but it take O(n) to traverse to the last node
        head_node = None
        last_node = None
        for item in iterable:
            new_node = Node(item, next_node=None)
            if head_node is None:
                head_node = new_node
            else:
                last_node.next_node = new_node
            last_node = new_node
        new = self.__class__()
        new.head = head_node
        self.__iadd__(new)

    @validate_args
    def find_middle(self) -> NodeType:
        """Return the node in the middle of the list. Raises ValueError if the linked list in empty."""
        if self.head is None:
            raise ValueError("{} is empty".format(type(self).__name__))

        slow = self.head
        fast = self.head
        while fast.next_node is not None and fast.next_node.next_node is not None:
            slow = slow.next_node
            fast = fast.next_node.next_node
        return slow

    @validate_args
    def has_cycle(self) -> bool:  # todo
        """Detect cycle(s) in the list."""
        # Floyd–Warshall algorithm
        raise NotImplementedError("todo")

    @validate_args
    def index(self, value: Any, start: int = 0, end: int = sys.maxsize) -> PositiveInt:  # todo
        """Return first index of value. Raises ValueError if the value is not present."""
        for idx, item in enumerate(self):
            if item == value:
                return idx  # noqa
        raise ValueError("{} not in {}".format(value, type(self).__name__))

    @validate_args
    def insert(self, idx: int, value: Any) -> None:
        """Create a new node with the given value and insert it before index."""
        # Time Complexity: O(1), but it take O(n) to traverse to the node at the index given

        new_node = Node(value=value, next_node=None)
        if idx == 0 or len(self) == 0:
            new_node.next_node = self.head
            self.head = new_node
        else:
            if idx < 0:
                prev_node = self.traverse(idx)
            else:
                prev_node = self.traverse(idx - 1)
            new_node.next_node = prev_node.next_node
            prev_node.next_node = new_node

    @validate_args
    def pop(self, idx: int) -> None:
        """Pop node at the index given."""
        # Time Complexity: O(1), but it take O(n) to traverse to the node at the index given

        if self.head is None:
            raise IndexError("pop from empty {}".format(type(self).__name__))
        if idx == 0:
            self.head = self.head.next_node
        prev_node = self.traverse(idx - 1)
        if prev_node.next_node is None:
            prev_node.next_node = None
        else:
            prev_node.next_node = prev_node.next_node.next_node

    @validate_args
    def remove(self, value: Any) -> None:  # todo
        """Remove first occurrence of value. Raises ValueError if the value is not present."""
        raise NotImplementedError("todo")

    @validate_args
    def remove_duplicates(self) -> None:
        """Remove duplicate item(s) in the list."""

        # Time Complexity: O(n) todo handle error

        def _remove_duplicates(current=None, previous=None, reference=None, iteration=0):
            iteration += 1
            if iteration > self.MAX_ITER:
                raise ExceededMaxIterations("Maximum number of iteration has been exceeded. Make sure there is no "
                                            "cycle in the linked list by using has_cycle() or increase "
                                            "MAX_ITER")
            if current is None:
                current = self.head
            if reference is None:
                reference = []
            if current.data in reference:
                temp = current.next_node
                if temp is not None:
                    while temp.value in reference:
                        temp = temp.next_node
                        if temp is None:
                            break
                previous.next_node = temp
            else:
                reference.append(current.data)
            if current.next_node is None:
                return
            return _remove_duplicates(current.next_node, current, reference, iteration)

        return _remove_duplicates()

    @validate_args
    def reverse(self) -> None:
        """Reverse a linked list."""
        # Time Complexity: O(n)

        prev_nd = None
        while self.head is not None:
            next_nd = self.head.next_node
            self.head.next_node = prev_nd
            prev_nd = self.head
            self.head = next_nd
        self.head = prev_nd

        # Recursive solution
        # def _reverse(cur_nd, prev_nd=None):
        #     if cur_nd is None:
        #         return prev_nd
        #
        #     next_nd = cur_nd.next_node
        #     cur_nd.next_node = prev_nd
        #     return _reverse(next_nd, cur_nd)
        #
        # self.head = _reverse(self.head)

    @validate_args
    def swap(self, idx1: int, idx2: int) -> None:
        """Swap two nodes at the indices given."""
        # Time Complexity: O(1)

        if idx1 == idx2:
            return
        if idx1 == 0 or idx2 == 0:
            prev2 = self.traverse(idx2 - 1 if idx1 == 0 else idx1 - 1)
            node2 = prev2.next_node
            self.head.next_node, node2.next_node = node2.next_node, self.head.next_node
            prev2.next_node = self.head
            self.head = node2
        else:
            prev1 = self.traverse(idx1 - 1)
            prev2 = self.traverse(idx2 - 1)
            node1 = prev1.next_node
            node2 = prev2.next_node
            prev1.next_node, prev2.next_node = prev2.next_node, prev1.next_node
            node1.next_node, node2.next_node = node2.next_node, node1.next_node

    @validate_args
    def traverse(self, idx: int) -> NodeType:
        """Loop through the linked list and get the node at the index given."""
        # Time Complexity: O(n), even for last k-th element

        for cur_idx, cur_item in enumerate(self):
            if idx < 0:
                if cur_idx == abs(idx) - 1:
                    target = self.head
                elif cur_idx > abs(idx) - 1:
                    target = target.next_node  # noqa
            elif cur_idx == idx:
                target = cur_item
                break

        if "target" not in locals():  # Check "target" is defined
            raise IndexError("{} index out of range".format(type(self).__name__))
        return target  # noqa
