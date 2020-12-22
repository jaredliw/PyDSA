from math import factorial, sqrt

from pydsa import validate_args, NonNegativeInt


@validate_args
def primarity_test(n: NonNegativeInt) -> bool:
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
