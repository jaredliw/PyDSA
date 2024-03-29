"""A linear data structure where each element is a separate object."""
import sys
from abc import ABC, abstractmethod
from copy import deepcopy
from operator import gt, lt

from pydsa import Any, Iterable, validate_args, PositiveInt, inherit_docstrings, Function
from pydsa.data_structures import Node, NodeType

__all__ = ["ExceedMaxIter", "SinglyLinkedList", "DoublyLinkedList"]


class ExceedMaxIter(RuntimeError):
    """Raised when maximum iterations has been exceeded. This is usually caused by a cycle inside a linked list."""
    pass


class _LinkedList(ABC):
    """A one-way linear data structure where elements are separated and non-contiguous objects that linked by \
    pointers.

    .. note:: Support all methods from built-in :code:`list`, except indexing / slicing.

    :ivar MAX_ITER: Maximum number of iterations, process will be terminated if it has been exceeded.
    :type MAX_ITER: int
    :ivar head: Head of linked list.
    :type head: Node or None
    :raises ExceededMaxIterations: Raised when maximum iterations has been exceeded to prevent an infinite loop.
    """
    __slots__ = ("MAX_ITER", "head")

    @validate_args
    def __init__(self, iterable: Iterable = None) -> None:
        """Initialize a new linked list from an iterable.

        :param iterable: An iterable to be converted into a linked list, default to None.
        :type iterable: Iterable or None
        """
        self.MAX_ITER = 99
        self.head = None

        if iterable is not None:
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

    def __iadd__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(
                "unsupported operand type(s) for +=: '{}' and '{}'".format(type(self).__name__, type(other).__name__))
        copied = other.copy()
        if self.head is None:
            self.head = copied.head
        else:
            node = self.traverse(-1)
            self._connect_nodes(node, copied.head)
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
                raise ExceedMaxIter("maximum number of iteration has been exceeded. Make sure there is no "
                                            "cycle in the linked list by using detect_cycle() or increase MAX_ITER")
            yield current
            # noinspection PyUnresolvedReferences
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
                super().__setattr__(key, value)
            else:
                raise ValueError(f"Value of '{key}' should be a(n) '{NodeType.__name__}', not '{type(value).__name__}'")
        elif key == "MAX_ITER":
            if isinstance(value, int):
                super().__setattr__(key, value)
            else:
                raise ValueError(f"Value of '{key}' should be a(n) '{NodeType.__name__}', not '{type(value).__name__}'")
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute {key}")

    def __str__(self):
        try:
            to_list = []
            for item in self:
                to_list.append(item.value)
            return f"{type(self).__name__}({str(to_list)})"
        except ExceedMaxIter:
            return f"{type(self).__name__}({'<cannot show node(s)>'})"

    def __repr__(self):
        try:
            return f"{type(self).__name__}({' -> '.join(map(lambda x: repr(x.value), self))})"
        except ExceedMaxIter:
            return f"{type(self).__name__}({'<cannot show node(s)>'})"

    @abstractmethod
    def _connect_nodes(self, node_a: NodeType, node_b: NodeType) -> None:
        pass

    @abstractmethod
    def _create_node(self, value: Any) -> NodeType:
        pass

    @validate_args
    def append(self, value: Any) -> None:
        """Append a new node to the end of linked list.

        Time complexity: :code:`O(1)`, but it take :code:`O(n)` to traverse to the last node.

        Space complexity: :code:`O(1)`.

        :param value: Value for new node.
        :type value: Any
        :rtype: None
        """
        new_node = self._create_node(value)
        if self.head is None:
            self.head = new_node
        else:
            tail_node = self.traverse(-1)
            self._connect_nodes(tail_node, new_node)

    @validate_args
    def clear(self) -> None:
        """Remove all nodes from linked list.

        Time complexity: :code:`O(1)`.

        Space complexity: :code:`O(1)`.

        :rtype: None
        """
        self.head = None

    @validate_args
    def copy(self):
        """Return a deep copy of linked list.

        Time complexity: :code:`O(n)`.

        Space complexity: :code:`O(n)`.

        :rtype: DoublyLinkedList / SinglyLinkedList
        """
        return deepcopy(self)

    @validate_args
    def count(self, value: Any) -> int:
        """Return number of occurrences of nodes with value.

        Time complexity: :code:`O(n)`.

        Space complexity: :code:`O(n)`.

        :param value: Value to count for.
        :type value: Any
        :returns: Number of occurrences.
        :rtype: int
        """
        counter = 0
        for item in self:
            if item == value:
                counter += 1
        return counter

    @validate_args
    def detect_cycle(self) -> [NodeType, None]:
        """Check whether linked list contains a cycle by Floyd's cycle-finding algorithm.

        Time complexity: :code:`O(n)`.

        Space complexity: :code:`O(1)`.

        :returns: The start node of the cycle. If there is no cycle, return None.
        :rtype: Node or None
        """
        if self.head is None:
            return None

        max_iter_copy = self.MAX_ITER
        self.MAX_ITER = sys.maxsize
        try:
            # Phase I
            fast_ptr = self.head
            slow_ptr = self.head
            while fast_ptr.next_node is not None and fast_ptr.next_node.next_node is not None:
                # fast_ptr moves two steps once while slow_ptr moves one step once
                # They will finally meet at some point if there is a cycle
                fast_ptr = fast_ptr.next_node.next_node
                slow_ptr = slow_ptr.next_node
                if fast_ptr is slow_ptr:
                    # Phase II
                    # Reset one pointer to the head
                    fast_ptr = self.head
                    while fast_ptr is not slow_ptr:
                        fast_ptr = fast_ptr.next_node  # fast_ptr is no longer "fast" now
                        slow_ptr = slow_ptr.next_node
                    # Two pointers will meet at the node where the cycle begins
                    return fast_ptr  # "return slow_ptr" does the job as well
            return None
        finally:
            self.MAX_ITER = max_iter_copy  # Reset MAX_ITER

    @validate_args
    def extend(self, iterable: Iterable) -> None:
        """Create nodes with values from iterable and extend them to the end of linked list.

        Time complexity: :code:`O(n)`, but it take :code:`O(n)` to traverse to the last node.

        Space complexity: :code:`O(n)`.

        :param iterable: An iterable of values to extend after the linked list.
        :type iterable: Iterable
        :rtype: None
        """
        last_node = None if self.head is None else self.traverse(-1)
        for item in iterable:
            new_node = self._create_node(item)
            if last_node is None:
                self.head = new_node
            else:
                self._connect_nodes(last_node, new_node)
            last_node = new_node

    @validate_args
    def find_middle(self) -> NodeType:
        """Return node at the middle of linked list, i.e. node at index :math:`\\lfloor\\frac{n}{2}\\rfloor`.

        Time complexity: :code:`O(n)`.

        Space complexity: :code:`O(1)`.

        :returns: Node at the middle of linked list.
        :rtype: Node
        :raises IndexError: Raised when linked list is empty.
        """
        if self.head is None:
            raise IndexError("{} is empty".format(type(self).__name__))

        slow = self.head
        fast = self.head
        while fast.next_node is not None and fast.next_node.next_node is not None:
            slow = slow.next_node
            fast = fast.next_node.next_node
        return slow

    @validate_args
    def index(self, value: Any, start: int = 0, end: int = sys.maxsize) -> PositiveInt:
        """Return first index of node with value. The optional arguments start and end are used to limit the search to \
        a particular subsequence of the linked list. The returned index is computed relative to the beginning of the \
        full sequence rather than the start argument.

        Time complexity: :code:`O(n)`

        Space Complexity: :code:`O(1)`

        :param value: Value to search for.
        :type value: Any
        :param start: Start of subsequence (inclusive), default to 0.
        :type start: int
        :param end: End of subsequence (exclusive), default to :code:`sys.maxsize`.
        :type end: int
        :returns: Index of node relative to the beginning of the full sequence.
        :rtype: int
        :raises ValueError: Raised when the value is not present.
        """

        def _index():
            nonlocal start
            if start < end:
                try:
                    node = self.traverse(start)
                except IndexError:
                    raise ValueError(f"{value} not in {type(self).__name__}")
                while node is not None and start < end:
                    if node == value:
                        return start
                    # noinspection PyUnresolvedReferences
                    node = node.next_node
                    start += 1
                raise ValueError(f"{value} not in {type(self).__name__}")
            else:
                raise ValueError(f"{value} not in {type(self).__name__}")

        if start >= 0 and end >= 0:
            # noinspection PyTypeChecker
            return _index()
        else:
            length = len(self)
            if start < 0 and end < 0:
                if -start > length:
                    return self.index(value, end=end)
                else:
                    # noinspection PyTypeChecker
                    return length + _index()  # Convert negative index to positive
            elif start < 0:  # Negative start, positive end
                return self.index(value, length + start, end)
            else:  # Positive start, negative end
                return self.index(value, start, length + end)

    @abstractmethod
    def insert(self, index: int, value: Any) -> None:
        """Create a new node with value and insert it before index.

        Time complexity: :code:`O(1)`, but it take :code:`O(n)` to traverse to the node at index.

        Space complexity: :code:`O(1)`.

        :param index: Index to insert a new node.
        :type index: int
        :param value: Value of the new node.
        :type value: Any
        :rtype: None
        """
        pass

    @abstractmethod
    def pop(self, index: int = -1) -> NodeType:
        """Remove and return node at index (default last). Raises :code:`IndexError` if list is empty or index is out \
        of range.

        Time complexity: :code:`O(1)`, but it takes `O(n)` to traverse to the node at index.

        Space complexity: :code:`O(1)`.

        :param index: Index of node to pop, default to -1.
        :type index: int
        :returns: Node at index.
        :rtype: Node
        :raises IndexError: Raised when linked list is empty or index is out of range.
        """
        pass

    @validate_args
    def remove(self, value: Any) -> None:
        """Remove first occurrence of node with value.

        :param value: Value to search for.
        :type value: Any
        :rtype: None
        :raises ValueError: Raised when the value is not present.
        """
        for idx, item in enumerate(self):
            if value == item:
                self.pop(idx)
                return
        raise ValueError("{} not in {}".format(value, type(self).__name__))

    @validate_args
    def remove_duplicates(self) -> None:
        """Remove node(s) with duplicated value(s) in linked list.

        Time complexity: :code:`O(n)`.

        Space complexity: :code:`O(n)`.

        :rtype: None
        :raises ExceededMaxIterations: Raised when MAX_ITER has been exceeded.
        """

        def _remove_duplicates(current=None, previous=None, reference=None, iteration=0):
            iteration += 1
            if iteration > self.MAX_ITER:
                raise ExceedMaxIter("Maximum number of iteration has been exceeded. Make sure there is no "
                                            "cycle in the linked list by using detect_cycle() or increase MAX_ITER")
            if current is None:
                current = self.head
            if reference is None:
                reference = []

            if current.value in reference:
                temp = current.next_node
                if temp is not None:
                    inner_iteration = 0
                    while temp.value in reference:
                        inner_iteration += 1
                        if inner_iteration > self.MAX_ITER:
                            raise ExceedMaxIter(
                                "Maximum number of iteration has been exceeded. Make sure there is no "
                                "cycle in the linked list by using detect_cycle() or increase MAX_ITER")
                        temp = temp.next_node
                        if temp is None:
                            break
                previous.next_node = temp
            else:
                reference.append(current.value)

            if current.next_node is None:
                return
            return _remove_duplicates(current.next_node, current, reference, iteration)

        if self.head is not None:
            return _remove_duplicates()

    @abstractmethod
    def reverse(self) -> None:
        """Reverse the linked list in place.

        Time complexity: :code:`O(n)`.

        Space complexity: :code:`O(1)`.

        :rtype: None
        """
        pass

    @validate_args
    def sort(self, key: Function = None, reverse: bool = False) -> None:
        """ Perform insertion sort in place.

        Time complexity: :code:`O(n^2)`.

        Space complexity: :code:`O(1)`.

        :param key: A function that serves as a key for the sort comparison, default to None.
        :type key: Callable
        :param reverse: The order of sorting, default to False i.e. ascending.
        :type reverse: bool
        :rtype: None
        """
        if self.head is None or self.head.next_node is None:
            return

        if reverse:
            cmp_func = gt
        else:
            cmp_func = lt
        if key is None:
            key = lambda x: x  # noqa

        dummy_node = self._create_node(-1)
        dummy_node.next_node = self.head

        next_ = self.head.next_node
        cur = self.head
        while next_ is not None:
            # No action needed, move forward
            if not cmp_func(key(next_.value), key(cur.value)):
                next_ = next_.next_node
                cur = cur.next_node
                continue
            # Start from the beginning, find the correct place for insertion
            correct_place = dummy_node
            while not cmp_func(key(next_.value), key(correct_place.next_node.value)):
                correct_place = correct_place.next_node
            # Insert
            self._connect_nodes(cur, next_.next_node)
            self._connect_nodes(next_, correct_place.next_node)
            self._connect_nodes(correct_place, next_)
            # Move forward
            next_ = cur.next_node
        self.head = dummy_node.next_node

    @abstractmethod
    def swap(self, index1: int, index2: int) -> None:
        """Swap two nodes at indices.

        Time complexity: :code:`O(1)`, but it takes :code:`O(n)` to traverse to the node.

        Space complexity: :code:`O(1)`.

        :param index1: Index of node 1.
        :type index1: int
        :param index2: Index of node 2.
        :type index2: int
        :rtype: None
        """
        pass

    @abstractmethod
    def traverse(self, index: int) -> NodeType:
        """Loop through the linked list and get the node at index.

        Time complexity: :code:`O(n)`, even for negative index.

        Space complexity: :code:`O(1)`.

        :param index: Index of node.
        :type index: int
        :returns: Node at index.
        :rtype: Node
        """
        pass


# noinspection PyMissingOrEmptyDocstring
@inherit_docstrings
class SinglyLinkedList(_LinkedList):
    def _connect_nodes(self, node_a: NodeType, node_b: NodeType) -> None:
        node_a.next_node = node_b

    def _create_node(self, value: Any) -> NodeType:
        return Node(value, next_node=None)

    @validate_args
    def insert(self, index: int, value: Any) -> None:
        new_node = self._create_node(value)
        if index == 0 or len(self) == 0:
            # noinspection PyTypeChecker
            self._connect_nodes(new_node, self.head)
            self.head = new_node
        else:
            try:
                prev_node = self.traverse(index - 1)
            except IndexError:
                if index > 0:  # if index (positive) >= length, append it at the end, same behavior as list.insert
                    return self.append(value)
                else:
                    return self.insert(0, value)
            # noinspection PyTypeChecker
            self._connect_nodes(new_node, prev_node.next_node)
            self._connect_nodes(prev_node, new_node)

    @validate_args
    def pop(self, index: int = -1) -> NodeType:
        if self.head is None:
            raise IndexError("pop from empty {}".format(type(self).__name__))

        if index == 0:
            self.head = self.head.next_node
            return self.head
        else:
            try:
                prev_node = self.traverse(index - 1)
            except IndexError as e:
                if self.traverse(index) is self.head:  # Check if node at index (negative) is a head node
                    return self.pop(0)
                else:
                    raise e
            if prev_node.next_node is None:
                raise IndexError(f"{type(self).__name__} index out of range")
            self._connect_nodes(prev_node, prev_node.next_node.next_node)
            return prev_node.next_node

    @validate_args
    def reverse(self) -> None:
        prev_nd = None
        iteration = 0
        while self.head is not None:
            iteration += 1
            if iteration > self.MAX_ITER:
                raise ExceedMaxIter("Maximum number of iteration has been exceeded. Make sure there is no "
                                            "cycle in the linked list by using detect_cycle() or increase MAX_ITER")
            next_nd = self.head.next_node
            self._connect_nodes(self.head, prev_nd)
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
    def swap(self, index1: int, index2: int) -> None:
        if index1 == index2:
            return
        elif index1 == 0 or index2 == 0:
            prev2 = self.traverse(index2 - 1 if index1 == 0 else index1 - 1)
            node2 = prev2.next_node
            if node2 is None:
                raise IndexError(f"{type(self).__name__} index out of range")
            self.head.next_node, node2.next_node = node2.next_node, self.head.next_node
            self._connect_nodes(prev2, self.head)
            self.head = node2
        else:
            prev1 = self.traverse(index1 - 1)
            prev2 = self.traverse(index2 - 1)
            node1 = prev1.next_node
            node2 = prev2.next_node
            prev1.next_node, prev2.next_node = node2, node1
            node1.next_node, node2.next_node = node2.next_node, node1.next_node

    @validate_args
    def traverse(self, index: int) -> NodeType:
        for cur_idx, cur_item in enumerate(self):
            if index < 0:
                if cur_idx == abs(index) - 1:
                    target = self.head
                elif cur_idx > abs(index) - 1:
                    # noinspection PyUnboundLocalVariable
                    target = target.next_node
            elif cur_idx == index:
                target = cur_item
                break

        if "target" not in locals():  # Check "target" is defined
            raise IndexError(f"{type(self).__name__} index out of range")
        # noinspection PyUnboundLocalVariable
        return target


# noinspection PyMissingOrEmptyDocstring
@inherit_docstrings
class DoublyLinkedList(_LinkedList):
    def _connect_nodes(self, node_a: [NodeType, None], node_b: [NodeType, None]) -> None:
        if node_a is not None:
            node_a.next_node = node_b
        if node_b is not None:
            node_b.last_node = node_a

    def _create_node(self, value: Any) -> NodeType:
        return Node(value, last_node=None, next_node=None)

    @validate_args
    def insert(self, index: int, value: Any) -> None:
        try:
            node_at_idx = self.traverse(index)
        except IndexError:
            if index > 0:
                self.append(value)
                return
            else:
                node_at_idx = self.head
        new_node = self._create_node(value)
        if node_at_idx is self.head:
            self.head = new_node
        else:
            last_node = node_at_idx.last_node
            # noinspection PyTypeChecker
            self._connect_nodes(last_node, new_node)
        # noinspection PyTypeChecker
        self._connect_nodes(new_node, node_at_idx)

    @validate_args
    def pop(self, index: int = -1) -> NodeType:
        node_at_idx = self.traverse(index)
        if node_at_idx is self.head:
            self.head = node_at_idx.next_node
        else:
            last_node = node_at_idx.last_node
            self._connect_nodes(last_node, node_at_idx.next_node)
        return node_at_idx

    @validate_args
    def reverse(self) -> None:
        if self.head is not None:
            cur_node = self.traverse(-1)
            self.head = cur_node

            while cur_node is not None:
                cur_node.last_node, cur_node.next_node = cur_node.next_node, cur_node.last_node
                cur_node = cur_node.next_node

    @validate_args
    def swap(self, index1: int, index2: int) -> None:
        if index1 == index2:
            return
        elif index1 == 0 or index2 == 0:
            node = self.traverse(index2 if index1 == 0 else index1)
            prev = node.last_node

            self.head.next_node, node.next_node = node.next_node, self.head.next_node
            prev.next_node = self.head
            if self.head.next_node is not None:
                self.head.next_node.last_node = self.head
            self.head.last_node = prev
            node.next_node.last_node = node
            node.last_node = None

            self.head = node
        else:
            node1 = self.traverse(index1)
            node2 = self.traverse(index2)
            prev1 = node1.last_node
            prev2 = node2.last_node

            prev1.next_node, prev2.next_node = node2, node1
            node1.next_node, node2.next_node = node2.next_node, node1.next_node
            if node1.next_node is not None:
                node1.next_node.last_node = node1
            node1.last_node = prev2
            node2.next_node.last_node = node2
            node2.last_node = prev1

    @validate_args
    def traverse(self, index: int) -> NodeType:
        if index >= 0:
            for idx, node in enumerate(self):
                if idx == index:
                    return node
                elif idx > index:
                    break
            raise IndexError("{} index out of range".format(type(self).__name__))
        else:
            end_node = None
            for end_node in self:
                pass
            # Traversing backwards
            idx = -1
            while end_node is not None:
                if idx == index:
                    return end_node
                # noinspection PyUnresolvedReferences
                end_node = end_node.last_node
                idx -= 1
            raise IndexError("{} index out of range".format(type(self).__name__))
