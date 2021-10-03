"""A collection of items stored at contiguous memory locations."""
from pydsa import Any, Iterable, NonNegativeInt, inherit_docstrings, validate_args
from copy import deepcopy
__all__ = ["ExceedMaxLengthError", "ConstantError", "StaticList", "DynamicList"]


class ExceedMaxLengthError(OverflowError):
    """Raised when length of a static list exceeds its limit."""
    pass


class ConstantError(ValueError):
    """Raised when trying to change a constant attribute."""
    pass


# noinspection PyMissingOrEmptyDocstring
@inherit_docstrings
class StaticList(list):
    """A continuous data structure that contains a group of elements with constant length.

    .. note:: All methods are inherited from :code:`list`, refer to :code:`help(list)` for a more explicit \
    documentation.

    :raises ExceedMaxLengthError: Raised when the length of list is exceeding \
    :attr:`~pydsa.data_structures.list.StaticList.max_length`.
    :raises ConstantError: Raised when trying to change the value of \
    :attr:`~pydsa.data_structures.list.StaticList.max_length`.
    """
    __slots__ = ("__max_length",)

    @validate_args
    def __init__(self, iterable: [Iterable, None] = None, max_length: [NonNegativeInt, None] = None):
        """Initialize a new static list from an iterable.

        :param iterable: An iterable to be converted into a static list, default to None.
        :type: Iterable or None
        :param max_length: Maximum length of list, default to the length of \
        :paramref:`~pydsa.data_structures.list.StaticList.__init__.iterable`.
        :raises ExceedMaxLengthError: Raised when the length of \
        :paramref:`~pydsa.data_structures.list.StaticList.__init__.iterable` is less than \
        :paramref:`~pydsa.data_structures.list.StaticList.__init__.max_length`.
        """
        if iterable is None:
            iterable = []

        super().__init__(list(iterable))

        if max_length is None:
            max_length = len(self)

        self.max_length = max_length
        if self.max_length < len(self):
            raise ExceedMaxLengthError(f"exceed static list maximum length: {self.max_length}")

    def __add__(self, other):
        new = deepcopy(self)
        new.__iadd__(other)
        return new

    def __eq__(self, other):
        return isinstance(other, self.__class__) and super().__eq__(other)

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __getattribute__(self, item):
        if item in ["append", "insert"] and super().__len__() + 1 > self.max_length:
            raise ExceedMaxLengthError(f"exceed static array maximum length: {self.max_length}")
        return super().__getattribute__(item)

    def __gt__(self, other):
        return not self.__lt__(other) and self.__ne__(other)

    def __iadd__(self, other):
        if not isinstance(other, StaticList):
            raise TypeError(f"can only concatenate {self.__class__.__name__} (not '{other.__class__.__name__}') to "
                            f"{self.__class__.__name__}")
        self.extend(other)
        return self

    def __imul__(self, other):
        if not isinstance(other, int):
            super().__imul__(other)  # Let list handle the error
        content = self[:]
        for _ in range(other - 1):
            self.extend(content)
        return self

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __lt__(self, other):
        return isinstance(other, self.__class__) and super().__lt__(other)

    def __mul__(self, other):
        new = deepcopy(other)
        new.__imul__(other)
        return new

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"{self.__class__.__name__}({super().__repr__()}, {self.max_length})"

    def __str__(self):
        return super().__repr__()

    @property
    def max_length(self):
        """Maximum length of list, cannot be changed after initializing.

        :type: int
        :raises ConstantError: Raised when trying to modify the value."""
        return self.__max_length

    @max_length.setter
    def max_length(self, value):
        try:
            print(self.__max_length)
        except AttributeError:
            self.__max_length = value
        else:
            raise ConstantError("StaticList.max_length is a constant")

    def copy(self):
        if self.__class__ == StaticList:  # For forward compatibility
            return self.__class__(super().copy(), self.max_length)
        else:
            return self.__class__(super().copy())

    def extend(self, iterable: Iterable) -> None:
        for item in iterable:
            if len(self) + 1 > self.max_length:
                raise ExceedMaxLengthError(f"exceed StaticList maximum length: {self.max_length}")
            super().append(item)


class _DynamicListMetaclass(type):
    """Overwriting __dir__ method for DynamicList class."""
    def __dir__(cls):
        return list(set(super().__dir__() + StaticList().__dir__()))


# noinspection PyMissingOrEmptyDocstring
@inherit_docstrings
class DynamicList(metaclass=_DynamicListMetaclass):
    """Growable static list. Conceptual, need not to use in Python.

    .. note:: All methods are inherited from :code:`list`, refer to :code:`help(list)` for a more explicit \
    documentation.
    """
    __slots__ = ("__container",)

    @validate_args
    def __init__(self, iterable: Iterable = None):
        """Initialize a new dynamic list from an iterable.

        :param iterable: An iterable to be converted into a static list, default to None.
        :type: Iterable or None
        """
        if iterable is None:
            iterable = []
        self.__container = iterable if isinstance(iterable, StaticList) else StaticList(iterable)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            other = other.__container
        return self.__class__(self.__container.__add__(other))

    def __delitem__(self, key):
        self.__container.__delitem__(key)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__container.__eq__(other.__container)
        else:
            return False

    def __dir__(self):
        return list(set(dir(self.__class__) + dir(self.__container)))

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __getattr__(self, item):
        cur_length = self.__container.__len__()
        max_length = self.__container.max_length
        if item in ['append', 'insert'] and cur_length + 1 > max_length:
            self.__expend_list()
        return getattr(self.__container, item)

    def __getitem__(self, item):
        return self.__container.__getitem__(item)

    def __gt__(self, other):
        return not self.__lt__(other) and self.__ne__(other)

    def __iter__(self):
        return self.__container.__iter__()

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __len__(self):
        return self.__container.__len__()

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.__container.__lt__(other.__container)
        else:
            return False

    def __mul__(self, other):
        return self.__class__(self.__container.__mul__(other))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__container.__str__()}, {self.__container.max_length})"

    def __reversed__(self):
        return self.__container.__reversed__()

    def __str__(self):
        return self.__container.__str__()

    def __expend_list(self) -> None:
        size = self.__container.max_length
        if size == 0:
            size = 1
        else:
            size *= 2
        self.__container = StaticList(self.__container[:], size)

    def __shrink_list(self) -> None:
        self.__container = StaticList(self.__container[:], self.__container.max_length // 2)

    def __post_check(self) -> None:
        if self.__len__() <= self.__container.max_length // 2:
            self.__shrink_list()

    @validate_args
    def clear(self) -> None:
        self.__container = StaticList()

    @validate_args
    def copy(self):
        return self.__class__(self.__container.copy())

    @validate_args
    def extend(self, iterable: Iterable) -> None:
        if not hasattr(iterable, "__len__"):
            length = len(list(iterable))
        else:
            length = len(iterable)
        while self.__len__() + length > self.__container.max_length:
            self.__expend_list()
        self.__container.extend(iterable)

    @validate_args
    def pop(self, index: int = -1) -> None:
        self.__container.pop(index)
        self.__post_check()

    @validate_args
    def remove(self, elem: Any) -> None:
        self.__container.remove(elem)
        self.__post_check()
