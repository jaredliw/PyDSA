"""An array is a collection of items stored at contiguous memory locations."""
from pydsa import Any, Iterable, NonNegativeInt, validate_args


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
            raise ExceedMaxLengthError("Exceed static array maximum length: {}".format(self.max_length))

    def __delattr__(self, item):
        raise AttributeError("Attribute '{}' could not be deleted".format(item))

    def __getattribute__(self, item):
        if item in ['append', 'insert'] and super(StaticArray, self).__len__() + 1 > self.max_length:
            raise ExceedMaxLengthError("Exceed static array maximum length: {}".format(self.max_length))
        return super(StaticArray, self).__getattribute__(item)

    def __repr__(self):
        return "StaticArray({}, {})".format(super(StaticArray, self).__repr__(), self.max_length)

    def __str__(self):
        return super(StaticArray, self).__repr__()

    @property
    def max_length(self):
        """A constant maximum length of StaticArray."""
        return self._max_length

    @max_length.setter
    def max_length(self, value):
        if not hasattr(self, "_max_length"):
            self._max_length = value
        else:
            raise ConstantError("StaticArray.max_length is a constant")

    @validate_args
    def copy(self):
        """Override list copy() function so that it returns a StaticArray object."""
        return StaticArray(super(StaticArray, self).copy(), self.max_length)

    @validate_args
    def extend(self, iterable: Iterable) -> None:
        """Override list extend() function to ensure the length of the list is always below self.max_length."""
        if len(self) + len(iterable) > self.max_length:
            raise ExceedMaxLengthError('Exceed StaticArray maximum length: {}'.format(self.max_length))
        super(StaticArray, self).extend(iterable)
