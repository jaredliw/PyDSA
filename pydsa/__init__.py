from inspect import isclass, Parameter, signature
from itertools import zip_longest
from typing import NewType

Function = NewType("Function", type(lambda x: None))
NonNegativeInt = NewType('NonNegativeInt', int)
PositiveInt = NewType('NaturalInt', int)
check_functs = {NonNegativeInt: lambda x: x >= 0,
                PositiveInt: lambda x: x >= 1}

class Empty:
    """Used for zip_longest.fillvalue to prevent collision with value None."""
    pass


def validate_args(f):
    """Validate function's argument(s) type."""

    def wrapper(*args, **kwargs):
        # Check args
        params = signature(f).parameters.values()
        for inp, accept in zip_longest(args, params, fillvalue=Empty()):
            arg_kind = accept.kind
            # Handle empty input
            if isinstance(inp, Empty):
                kwarg = kwargs.get(accept.name)
                if kwarg is not None:
                    inp = kwarg
                # Chekc if there is an default argument
                elif type(accept.default) != type(type) and arg_kind == Parameter.POSITIONAL_OR_KEYWORD:
                    continue
                elif arg_kind in [Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD]:
                    continue
            if isinstance(inp, Empty) or isinstance(accept, Empty):
                raise TypeError("{} expected {} arguments, got {}".format(f.__name__, len(params), len(args)))

            inp_type = type(inp)
            accept_types = accept.annotation

            if not isinstance(accept_types, list):
                accept_types = [accept_types]

            for at in accept_types:
                # Relpace None with NoneType
                if at is None:
                    at = type(None)

                _at = at
                # Check if annotation is 'NewType'
                if not isclass(at):
                    at = at.__supertype__

                if inp_type == at:
                    matching_type = _at
                    break
            else:
                if type(accept_types) == list:
                    message = " or ".join(("'{}'".format(t.__name__) for t in accept_types))
                raise TypeError(
                    "{} accepts {} as {}, not '{}'".format(f.__name__, message, accept.name, inp_type.__name__))

            to_test = check_functs.get(matching_type)
            if (to_test is not None) and (not to_test(inp)):
                raise ValueError("{} is not a(n) '{}'".format(inp, matching_type.__name__))

        # Call fuction
        ret = f(*args, **kwargs)
        return ret

    return wrapper

# Notes for PyDSA-styled annotations:
# - If there is built-in type avaliable, don't hesistate to use it
# - For logic OR, write it like this: "[int, str]" rather than "int or str"
# - Do not use typing module (The items from there has insufficient infomation for argument validation)
#       - Use collection.Sequence to replace typing.Sequence (annotate for iterable)
# - Define a new type if there is no avalaible type to use
#       - Use Function defined above rather than typing.Callable
