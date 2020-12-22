from inspect import isclass, signature
from itertools import zip_longest
from typing import NewType

NonNegativeInt = NewType('NonNegativeInt', int)
PositiveInt = NewType('NaturalInt', int)
check_functs = {NonNegativeInt: lambda x: x >= 0,
                PositiveInt: lambda x: x >= 1}

class Empty:
    """Used for zip_longest.fillvalue to prevent collision with value None."""
    pass


def validate_args(f):
    """Validate function's argument(s) type."""

    def wrapper(*args):
        # Check args
        params = signature(f).parameters.values()
        for inp, accept in zip_longest(args, params, fillvalue=Empty):
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
                    "{} accepts {} as n, not '{}'".format(f.__name__, message, inp_type.__name__))

            to_test = check_functs.get(matching_type)
            if (to_test is not None) and (not to_test(inp)):
                raise ValueError("{} is not a(n) '{}'".format(inp, matching_type.__name__))

        # Call fuction
        ret = f(*args)
        return ret

    return wrapper

# Use "[int, str]" to replace "int or str" for annotations, meaning either int or str.
# inspect.signature.parameters cannot catch the second value if you use "or".
