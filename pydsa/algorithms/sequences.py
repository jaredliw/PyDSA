"""A sequence is an enumerated collection of objects in which repetitions are allowed and order matters."""
from pydsa import NonNegativeInt, validate_args

__all__ = ["fibonacci"]

# todo: use formula to get nth fibonacci --> ((1+sqrt(5))**n - (1-sqrt(5))**n) / (2**n * sqrt(5))
@validate_args
def fibonacci(n: NonNegativeInt, value1: [int, float] = 0, value2: [int, float] = 1) -> [int, float]:
    """Get the nth fibonacci number, starting with value1 and value2 given."""
    if n == 0:
        return value1
    for _ in range(1, n):
        value1, value2 = value2, value1 + value2
    return value2
