"""All algorithms about mathematics."""
from functools import reduce
from math import factorial, sqrt

from pydsa import validate_args, NonNegativeInt, PositiveInt

__all__ = ["primality_test", "wilsons_theorem", "gcd", "lcm", "digital_root", "ackermann_peter", "fibonacci"]


@validate_args
def primality_test(n: PositiveInt) -> bool:
    """Determine whether a number is a prime."""

    # Optimization 1: Test from 2 to sqrt(n) only, since a factor will appear twice when we test from 2 to n.
    # Optimization 2: Do not test even numbers except 2, since all even numbers is divisible by 2.

    # Optimization 3: Check though 2, 3 and all numbers in the form 6k + 1 <= sqrt(n) only. (Three times faster)
    # Why?
    # Observe that all primes greater than 3 are of the form 6k ± 1, where k is any integer greater than 0. This is
    # because all integers can be expressed as (6k + i), where i = −1, 0, 1, 2, 3, or 4. Note that 2 divides (6k + 0),
    # (6k + 2), and (6k + 4) and 3 divides (6k + 3). -- Wikipedia

    if n == 1:
        raise ArithmeticError("1 is neither a prime nor a composite")
    elif n == 2 or n == 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    else:
        bound = int(sqrt(n))
        k = 1
        while 6 * k - 1 <= bound:
            if n % (6 * k - 1) == 0 or n % (6 * k + 1) == 0:
                return False
            k += 1
        return True


@validate_args
def wilsons_theorem(n: NonNegativeInt) -> bool:
    """In number theory, Wilson's theorem states that a natural number n > 1 is a prime number if and only if the
    product of all the positive integers less than n is one less than a multiple of n. -- Wikipedia"""
    # (n - 1)! ≡ -1 (mod n)
    # Not practical

    if n == 1:
        raise ArithmeticError("1 is neither a prime nor a composite")
    else:
        return (factorial(n - 1) + 1) % n == 0


@validate_args
def gcd(a: int, b: int, *num: int) -> int:
    """The greatest common divisor (GCD) of two or more integers, which are not all zero, is the largest positive
    integer that divides each of the integers. -- Wikipedia"""

    # Time Complexity: O(log(a+b)), for two integers, a and b
    # GCD(a, b) = (|a * b|) / LCM(a, b)

    def _gcd(x, y):
        if x == 0:
            if y == 0:
                raise ArithmeticError("GCD of 0 and 0 is undefined")
            return abs(y)
        else:
            return _gcd(y % x, x)

    b = _gcd(a, b)
    while len(num) != 0:
        b = _gcd(b, num[0])
        num = num[1:]
    return b


@validate_args
def lcm(a: int, b: int, *num: int) -> int:
    """The lowest common multiple (LCM) is the smallest positive integer that is evenly divisible by both a and b.
    -- Wikipedia"""

    # Time Complexity: O(log(a+b)), for two integers, a and b
    # LCM(a, b) = (|a * b|) / GCD(a, b)

    def _lcm(x, y):
        if x == 0 or y == 0:
            raise ArithmeticError("LCM of {} and {} is undefined".format(x, y))
        return abs(x * y) // gcd(x, y)

    return reduce(_lcm, [a, b, *num])


@validate_args
def digital_root(num: NonNegativeInt) -> int:
    """The digital root (also repeated digital sum) of a natural number in a given number base is the (single digit)
    value obtained by an iterative process of summing digits, on each iteration using the result from the previous
    iteration to compute a digit sum. -- Wikipedia

    For example: 154 -> 1 + 5 + 4 = 10 -> 1 + 0 = 1
    """
    # https://en.wikipedia.org/wiki/Digital_root
    # Direct formula:
    #            r 0                        , if n = 0
    # dr_b(n) = <
    #            L 1 + ((n - 1) mod (b - 1)), if n != 0
    return 0 if num == 0 else (1 + (num - 1) % 9)


@validate_args
def ackermann_peter(m: NonNegativeInt, n: NonNegativeInt) -> PositiveInt:
    """
    Definition
              r    n + 1,                m = 0
     A(m, n) <     A(m - 1 , 1),         m > 0 and n = 0
              L    A(m - 1, A(m, n-1))   m > 0 and n > 0
    """
    if m == 0:
        return n + 1  # noqa
    elif n == 0:
        return ackermann_peter(m - 1, 1)  # noqa
    else:
        return ackermann_peter(m - 1, ackermann_peter(m, n - 1))  # noqa


# todo: use formula to get nth fibonacci --> ((1+sqrt(5))**n - (1-sqrt(5))**n) / (2**n * sqrt(5))
@validate_args
def fibonacci(n: NonNegativeInt, value1: [int, float] = 0, value2: [int, float] = 1) -> [int, float]:
    """Get the nth fibonacci number, starting with value1 and value2 given."""
    if n == 0:
        return value1
    for _ in range(1, n):
        value1, value2 = value2, value1 + value2
    return value2
