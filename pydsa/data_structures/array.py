"""An array is a collection of items stored at contiguous memory locations."""
from pydsa import Any, Iterable, NonNegativeInt, validate_args

__all__ = ["ExceedMaxLengthError", "ConstantError", "StaticArray", "DynamicArray", "List"]


class ExceedMaxLengthError(OverflowError):
    """Raised when the length of an array exceeds its limit."""
    pass


class ConstantError(ValueError):
    """Raised when trying to change a constant variable."""
    pass


class StaticArray(list):
    """Array with static length."""

    @validate_args
    def __init__(self: None, arr: [Iterable, None] = None, max_length: [NonNegativeInt, None] = None):
        if arr is None:
            arr = []

        super(StaticArray, self).__init__(list(arr))

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
        """A constant maximum length of StaticArray."""
        return self.__max_length

    @max_length.setter
    def max_length(self, value):
        if not hasattr(self, "_{}__max_length".format(self.__class__.__name__)):
            self.__max_length = value
        else:
            raise ConstantError("StaticArray.max_length is a constant")

    @validate_args
    def copy(self):
        """Override list copy() function so that it returns a StaticArray object."""
        if self.__class__ == StaticArray:
            return self.__class__(super(StaticArray, self).copy(), self.max_length)
        else:
            return self.__class__(super(StaticArray, self).copy())

    @validate_args
    def extend(self, iterable: Iterable) -> None:
        """Override list extend() function to ensure the length of the list is always below self.max_length."""
        if len(self) + len(list(iterable)) > self.max_length:
            raise ExceedMaxLengthError('exceed StaticArray maximum length: {}'.format(self.max_length))
        super(StaticArray, self).extend(iterable)


class DynamicArray(StaticArray):
    """Array (implemented on StaticArray) with dynamic length."""

    # Conceptual, need not to use in Python.

    @validate_args
    def __init__(self, arr: Iterable = None):
        if arr is None:
            arr = []
        super(DynamicArray, self).__init__(arr)

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
    def clear(self) -> None:
        """Override StaticArray clear() function so that the qarray will shrink."""
        super(DynamicArray, self).__init__([])

    @validate_args
    def pop(self, index: int = -1) -> None:
        """Override StaticArray pop() function so that the list shrink when element is removed."""
        old_length = self.max_length
        super(DynamicArray, self).pop(index)
        if self.__len__() <= old_length // 2:
            self.__shrink_array(old_length)

    @validate_args
    def extend(self, iterable: Iterable) -> None:
        """Override StaticArray extend() function to expand the list when exceeding the max_length of StaticArray."""
        if not hasattr(iterable, "__len__"):
            length = len(list(iterable))
        else:
            length = len(iterable)
        while self.__len__() + length > self.max_length:
            self.__expend_array()
        super(DynamicArray, self).extend(iterable)

    @validate_args
    def remove(self, elem: Any) -> None:
        """Override list remove() function so that the list shrink when element is removed."""
        old_length = self.max_length
        super(DynamicArray, self).remove(elem)
        if self.__len__() <= old_length // 2:
            self.__shrink_array(old_length)


class List(list):
    """Extended functionalities for python list."""

    @validate_args
    def rotate(self, k: int) -> None:
        """Rotate the elements to the left by k. (Negative k means right rotation)"""
        # Faster than collections.deque.rotate
        if len(self) != 0:
            k %= len(self)
            self.__init__(self[k:] + self[:k])
