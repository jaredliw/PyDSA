"""A function is a process or a relation that associates each element x of a set X, the domain of the function, to a
single element y of another set Y (possibly the same set), the codomain of the function."""
from typing import NewType

NonNegativeInt = NewType('NonNegativeInt', int)

def ackermann_peter(m: NonNegativeInt, n: NonNegativeInt) -> NonNegativeInt:
    """
    Definition
              r    n + 1,                m = 0
     A(m, n) <     A(m - 1 , 1),         m > 0 and n = 0
              L    A(m - 1, A(m, n-1))   m > 0 and n > 0
    """

    # Validation
    if type(m) != int or type(n) != int:
        raise TypeError("m and n should be integers, not '{}' and '{}'".format(type(m).__name__,
                                                                               type(n).__name__))
    elif m < 0 or n < 0:
        raise ValueError("m and n should be non-negative, not '{}' and '{}'".format(m, n))

    # Main function
    if m == 0:
        return n + 1
    elif n == 0:
        return ackermann_peter(m - 1, 1)
    else:
        return ackermann_peter(m - 1, ackermann_peter(m, n - 1))
