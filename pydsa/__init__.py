from inspect import isclass, Parameter, signature
from itertools import zip_longest
from typing import NewType


class _Any:
    def __eq__(self, other):
        return True


class _Function:
    def __eq__(self, other):
        return callable(other)


class _Iterable:
    def __eq__(self, other):
        return hasattr(other, "__iter__")


class _Sequence:
    def __eq__(self, other):
        return hasattr(other, "__getitem__") and hasattr(other, "__len__")


Any = NewType("Any", _Any())
Function = NewType("Function", _Function())
Iterable = NewType("Iterable", _Iterable())
Sequence = NewType("Sequence", _Sequence())
IntFloatSequence = NewType("IntFloatSequence", _Sequence())
NonNegativeInt = NewType('NonNegativeInt', int)
PositiveInt = NewType('NaturalInt', int)
check_functs = {IntFloatSequence: lambda x: all(type(item) in [int, float] for item in x),
                NonNegativeInt: lambda x: x >= 0,
                PositiveInt: lambda x: x >= 1}


def validate_args(f):
    """Validate function's argument(s) type."""

    def _wrapper(*args, **kwargs):
        # Check args
        params = signature(f).parameters.values()
        for idx, [inp, accept] in enumerate(zip_longest(args, params, fillvalue=Parameter.empty)):
            message = ""
            if idx == 0 and "." in f.__qualname__:
                continue
            # Handle empty input
            if inp == Parameter.empty:
                kwarg = kwargs.get(accept.name)
                if kwarg is not None:
                    inp = kwarg
                else:
                    continue

            inp_type = type(inp)
            if accept == Parameter.empty:
                continue
            accept_types = accept.annotation

            if accept_types == Parameter.empty:
                continue
            elif not isinstance(accept_types, list):
                accept_types = [accept_types]

            for at in accept_types:
                # Relpace None with NoneType
                if at is None:
                    at = type(None)

                _at = at
                # Check if annotation is 'NewType'
                if not isclass(at):
                    at = at.__supertype__

                if at == inp_type:
                    matching_type = _at
                    break
            else:
                if type(accept_types) == list:
                    message = " or ".join(("'{}'".format(t if t is None else t.__name__) for t in accept_types))
                raise TypeError(
                    "{} accepts {} as {}, not '{}'".format(f.__name__, message, accept.name, inp_type.__name__))

            to_test = check_functs.get(matching_type)
            if (to_test is not None) and (not to_test(inp)):
                raise ValueError("{} is not a(n) '{}'".format(inp, matching_type.__name__))

        # Call fuction
        ret = f(*args, **kwargs)
        return ret

    return _wrapper

# Notes for PyDSA-styled annotations:
# - If there is built-in type avaliable, don't hesistate to use it
# - For logic OR, write it like this: "[int, str]" rather than "int or str"
# - Do not use typing module (The items from there has insufficient infomation for argument validation)
# - Define a new type if there is no avalaible type to use
#       - Use Function defined above rather than typing.Callable
# - Do not use "from __future__ import annotations"
