"""A collection of items stored at contiguous memory locations."""
import math

from pydsa import Any, Iterable, NonNegativeInt, inherit_docstrings, validate_args
from copy import deepcopy, copy

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
        if not isinstance(other, self.__class__):
            raise TypeError(f"can only concatenate {self.__class__.__name__} (not '{other.__class__.__name__}') to "
                            f"{self.__class__.__name__}")
        self.extend(other)
        return self

    def __imul__(self, other):
        if not isinstance(other, int):
            super().__imul__(other)  # Let list handles the exception
        if other < 1:  # Fun fact: [...] * -1 => []
            self.clear()
            return self

        content = self[:]
        for _ in range(other - 1):
            self.extend(content)
        return self

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __lt__(self, other):
        return isinstance(other, self.__class__) and super().__lt__(other)

    def __mul__(self, other):
        new = deepcopy(self)
        new.__imul__(other)
        return new

    def __ne__(self, other):
        return not self.__eq__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

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
            self.__max_length
        except AttributeError:
            self.__max_length = value
        else:
            raise ConstantError(f"{self.__class__.__name__}.max_length is a constant")

    @validate_args
    def copy(self):
        return copy(self)  # shallow copy

    @validate_args
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
        new = deepcopy(self)
        new.__iadd__(other)
        return new

    def __copy__(self):
        new = self.__class__.__new__(self.__class__)
        new.__container = self.__container
        return new

    def __deepcopy__(self, memodict):
        new = self.__class__.__new__(self.__class__)
        new.__container = self.__container.__class__(self.__container[:], self.max_length)
        return new

    def __delattr__(self, item):
        try:
            if item in dir(StaticList):
                self.__container.__class__.__dict__[item].__delete__(item)
            else:
                self.__class__.__dict__[item].__delete__(item)
        except KeyError:
            raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{item}'")

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
        if item in ['append', 'insert'] and self.__len__() + 1 > self.max_length:
            self.__create_new_container(length=self.__len__() + 1)
        try:
            return getattr(self.__class__, item)
        except AttributeError:
            try:
                return getattr(self.__container, item)
            except AttributeError:
                pass  # Do not raise error here, prevent nested exceptions
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")

    def __getitem__(self, item):
        return self.__container.__getitem__(item)

    def __gt__(self, other):
        return not self.__lt__(other) and self.__ne__(other)

    def __iadd__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(f"can only concatenate {self.__class__.__name__} (not '{other.__class__.__name__}') to "
                            f"{self.__class__.__name__}")
        self.extend(other)
        return self

    def __imul__(self, other):
        if isinstance(other, int):
            if other < 1:
                self.__create_new_container([], 0)
            elif self.__len__() * other > self.max_length:
                self.__create_new_container(length=self.__len__() * other)
        self.__container.__imul__(other)
        return self

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
        new = deepcopy(self)
        new.__imul__(other)
        return new

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__container.__str__()}, {self.max_length})"

    def __reversed__(self):
        return self.__container.__reversed__()

    def __rmul__(self, other):
        return self.__mul__(other)

    def __setattr__(self, key, value):
        try:
            if key in dir(StaticList):
                self.__container.__class__.__dict__[key].__set__(self, value)
            else:
                self.__class__.__dict__[key].__set__(self, value)
        except KeyError:
            raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{key}'")

    def __str__(self):
        return self.__container.__str__()

    @property
    def max_length(self):
        return self.__container.max_length

    @max_length.setter
    def max_length(self, value):
        self.__container.max_length = value

    def __create_new_container(self, content=None, length=None):
        if content is None:
            content = self.__container[:]
        if length is None:
            length = self.__len__()
        self.__container = StaticList(content, 0 if length == 0 else 2 ** math.ceil(math.log2(length)))

    @validate_args
    def copy(self):
        return copy(self)

    @validate_args
    def clear(self) -> None:
        self.__create_new_container([], 0)

    @validate_args
    def extend(self, iterable: Iterable) -> None:
        init_length = self.__len__()
        for item in iterable:
            if init_length + 1 > self.max_length:
                self.__create_new_container(length=init_length + 1)
            self.__container.append(item)
            init_length += 1

    @validate_args
    def pop(self, index: int = -1) -> None:
        self.__container.pop(index)
        self.__create_new_container()

    @validate_args
    def remove(self, elem: Any) -> None:
        self.__container.remove(elem)
        self.__create_new_container()
