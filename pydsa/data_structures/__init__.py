from typing import NewType

from pydsa import Any, check_arg, validate_args

__all__ = ["NodeType", "Node"]


class _NodeType:
    def __eq__(self, other):
        # Cannot directly use isinstance(other, Node) here, since 'other' is a type object,
        # type() of two instances of a class is equal
        node = Node()
        return other == type(node)


NodeType = NewType("NodeType", _NodeType())


class Node:
    """A fundamental unit of which graphs/linked lists etc. are formed."""

    __annots = {}

    @validate_args
    def __init__(self, value: Any = None, **attr):
        self.value = value
        if attr is not None:
            for key, _value in attr.items():
                self.__annots[key] = Any
                self.__dict__[key] = _value

    def __delattr__(self, item):
        raise TypeError("cannot delete attribute '{}'".format(item))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            other = other.value

        return self.value == other

    def __ge__(self, other):
        return not self.__lt__(other)

    def __gt__(self, other):
        return not self.__le__(other)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            other = other.value

        return self.value < other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __setattr__(self, key, value):
        if key == "value":
            self.__dict__[key] = value
        else:
            annots = self.__annots.get(key)
            if annots is None:
                raise AttributeError("{} has no attribute '{}'".format(self.__class__.__name__, key))
            check_arg(key, value, annots)
            self.__dict__[key] = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        if type(self.value) == str:
            value = "'{}'".format(self.value)
        else:
            value = self.value
        return "{}({})".format(self.__class__.__name__, value)

    @validate_args
    def set_annotations(self, **annot: dict) -> None:
        """Annotate the attribute(s) and it will validate value(s) when calling __setattr__."""
        for name, _type in annot.items():
            if name in self.__annots:
                self.__annots[name] = _type
            else:
                raise AttributeError("{} has no attribute '{}'".format(self.__class__.__name__, name))
