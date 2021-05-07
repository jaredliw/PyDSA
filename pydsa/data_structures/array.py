"""A collection of items stored at contiguous memory locations."""
from pydsa import Any, Iterable, NonNegativeInt, validate_args

__all__ = ["ExceedMaxLengthError", "ConstantError", "StaticArray", "DynamicArray", "List"]


class ExceedMaxLengthError(OverflowError):
    """Raised when length of a static array exceeds its limit."""
    pass


class ConstantError(ValueError):
    """Raised when trying to change a constant attribute."""
    pass


class StaticArray(list):
    """A continuous data structure that contains a group of elements with constant length.

    .. note:: All methods are inherited from :code:`list`, refer to :code:`help(list)` for a more explicit \
    documentation.

    :raises ExceedMaxLengthError: Raised when the length of array is exceeding \
    :attr:`~pydsa.data_structures.array.StaticArray.max_length`.
    :raises ConstantError: Raised when trying to change the value of \
    :attr:`~pydsa.data_structures.array.StaticArray.max_length`.
    """

    @validate_args
    def __init__(self, iterable: [Iterable, None] = None, max_length: [NonNegativeInt, None] = None):
        """Initialize a new static array from an iterable.

        :param iterable: An iterable to be converted into a static array, default to None.
        :type: Iterable or None
        :param max_length: Maximum length of array, default to the length of \
        :attr:`~pydsa.data_structures.array.StaticArray.iterable`.
        :raises ExceedMaxLengthError: Raised when the length of \
        :attr:`~pydsa.data_structures.array.StaticArray.iterable` is less than \
        :attr:`~pydsa.data_structures.array.StaticArray.max_length`.
        """
        if iterable is None:
            iterable = []

        super(StaticArray, self).__init__(list(iterable))

        if max_length is None:
            max_length = len(self)

        self.max_length = max_length
        if self.max_length < len(self):
            raise ExceedMaxLengthError("exceed static array maximum length: {}".format(self.max_length))

    def __add__(self, other):
        return self.__class__(super(StaticArray, self).__add__(other))

    def __delattr__(self, item):
        raise AttributeError("attribute '{}' could not be deleted".format(item))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and super(StaticArray, self).__eq__(other)

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __getattribute__(self, item):
        if item in ["append", "insert"] and super(StaticArray, self).__len__() + 1 > self.max_length:
            raise ExceedMaxLengthError("exceed static array maximum length: {}".format(self.max_length))
        return super(StaticArray, self).__getattribute__(item)

    def __gt__(self, other):
        return not self.__lt__(other)

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __lt__(self, other):
        return isinstance(other, self.__class__) and super(StaticArray, self).__le__(other)

    def __mul__(self, other):
        return self.__class__(super(StaticArray, self).__mul__(other))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "{}({}, {})".format(self.__class__.__name__, super(StaticArray, self).__repr__(), self.max_length)

    def __str__(self):
        return super(StaticArray, self).__repr__()

    @property
    def max_length(self):
        """Maximum length of array, cannot be changed after initializing.

        :type: int
        :raises ConstantError: Raised when trying to modify the value."""
        return self.__max_length

    @max_length.setter
    def max_length(self, value):
        if not hasattr(self, "_{}__max_length".format(self.__class__.__name__)):
            self.__max_length = value
        else:
            raise ConstantError("StaticArray.max_length is a constant")

    def copy(self):  # noqa
        self.__doc__ = super(StaticArray, self).copy.__doc__

        if self.__class__ == StaticArray:
            return self.__class__(super(StaticArray, self).copy(), self.max_length)
        else:
            return self.__class__(super(StaticArray, self).copy())

    def extend(self, iterable: Iterable) -> None:  # noqa
        self.__doc__ = super(StaticArray, self).copy.__doc__

        if len(self) + len(list(iterable)) > self.max_length:
            raise ExceedMaxLengthError('exceed StaticArray maximum length: {}'.format(self.max_length))
        super(StaticArray, self).extend(iterable)


class DynamicArray(StaticArray):
    """Growable static array. Conceptual, need not to use in Python.

    .. note:: All methods are inherited from :code:`list`, refer to :code:`help(list)` for a more explicit \
    documentation.
    """

    @validate_args
    def __init__(self, iterable: Iterable = None):
        """Initialize a new static array from an iterable.

        :param iterable: An iterable to be converted into a static array, default to None.
        :type: Iterable or None
        """
        if iterable is None:
            iterable = []
        super(DynamicArray, self).__init__(iterable)

    def __getattribute__(self, item):
        if item in ['append', 'insert'] and self.__len__() + 1 > self.max_length:
            self.__expend_array()
        return super(DynamicArray, self).__getattribute__(item)

    @validate_args
    def __expend_array(self) -> None:
        size = self.max_length
        if size == 0:
            size = 1
        else:
            size *= 2
        super(DynamicArray, self).__init__(self, size)

    @validate_args
    def __shrink_array(self, old_length: int) -> None:
        size = old_length // 2
        super(DynamicArray, self).__init__(self, size)

    @validate_args
    def clear(self) -> None:  # noqa
        self.__doc__ = super(DynamicArray, self).clear.__doc__

        super(DynamicArray, self).__init__([])

    @validate_args
    def pop(self, index: int = -1) -> None:  # noqa
        self.__doc__ = super(DynamicArray, self).pop.__doc__

        old_length = self.max_length
        super(DynamicArray, self).pop(index)
        if self.__len__() <= old_length // 2:
            self.__shrink_array(old_length)

    @validate_args
    def extend(self, iterable: Iterable) -> None:  # noqa
        self.__doc__ = super(DynamicArray, self).extend.__doc__

        if not hasattr(iterable, "__len__"):
            length = len(list(iterable))
        else:
            length = len(iterable)
        while self.__len__() + length > self.max_length:
            self.__expend_array()
        super(DynamicArray, self).extend(iterable)

    @validate_args
    def remove(self, elem: Any) -> None:  # noqa
        self.__doc__ = super(DynamicArray, self).remove.__doc__

        old_length = self.max_length
        super(DynamicArray, self).remove(elem)
        if self.__len__() <= old_length // 2:
            self.__shrink_array(old_length)
