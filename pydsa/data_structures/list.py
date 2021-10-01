"""A collection of items stored at contiguous memory locations."""
from pydsa import Any, Iterable, NonNegativeInt, validate_args

__all__ = ["ExceedMaxLengthError", "ConstantError", "StaticList", "DynamicList"]


class ExceedMaxLengthError(OverflowError):
    """Raised when length of a static list exceeds its limit."""
    pass


class ConstantError(ValueError):
    """Raised when trying to change a constant attribute."""
    pass


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

        super(StaticList, self).__init__(list(iterable))

        if max_length is None:
            max_length = len(self)

        self.max_length = max_length
        if self.max_length < len(self):
            raise ExceedMaxLengthError("exceed static list maximum length: {}".format(self.max_length))

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
            return self.__class__(super(StaticList, self).copy(), self.max_length)
        else:
            return self.__class__(super(StaticList, self).copy())

    def extend(self, iterable: Iterable) -> None:
        if len(self) + len(list(iterable)) > self.max_length:
            raise ExceedMaxLengthError('exceed StaticList maximum length: {}'.format(self.max_length))
        super(StaticList, self).extend(iterable)


class DynamicList(StaticList):
    """Growable static list. Conceptual, need not to use in Python.

    .. note:: All methods are inherited from :code:`list`, refer to :code:`help(list)` for a more explicit \
    documentation.
    """

    @validate_args
    def __init__(self, iterable: Iterable = None):
        """Initialize a new static list from an iterable.

        :param iterable: An iterable to be converted into a static list, default to None.
        :type: Iterable or None
        """
        if iterable is None:
            iterable = []
        super(DynamicList, self).__init__(iterable)

    def __getattribute__(self, item):
        if item in ['append', 'insert'] and self.__len__() + 1 > self.max_length:
            self.__expend_list()
        return super(DynamicList, self).__getattribute__(item)

    @validate_args
    def __expend_list(self) -> None:
        size = self.max_length
        if size == 0:
            size = 1
        else:
            size *= 2
        print(super())
        print(self[:])
        print("a", super(DynamicList, self).__class__())
        print(self[:])
        # super(DynamicList, self).__init__(self, size)

    @validate_args
    def __shrink_list(self, old_length: int) -> None:
        size = old_length // 2
        super().__new__(self[:], size)
        # super(DynamicList, self).__init__(self, size)

    @validate_args
    def clear(self) -> None:
        super(DynamicList, self).__init__([])

    @validate_args
    def pop(self, index: int = -1) -> None:
        old_length = self.max_length
        super(DynamicList, self).pop(index)
        if self.__len__() <= old_length // 2:
            self.__shrink_list(old_length)

    @validate_args
    def extend(self, iterable: Iterable) -> None:
        if not hasattr(iterable, "__len__"):
            length = len(list(iterable))
        else:
            length = len(iterable)
        while self.__len__() + length > self.max_length:
            self.__expend_list()
        super(DynamicList, self).extend(iterable)

    @validate_args
    def remove(self, elem: Any) -> None:
        old_length = self.max_length
        super(DynamicList, self).remove(elem)
        if self.__len__() <= old_length // 2:
            self.__shrink_list(old_length)
