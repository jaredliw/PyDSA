from pydsa.algorithms.math import *
from tests import is_error

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103,
          107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223,
          227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347,
          349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
          467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607,
          613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743,
          751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883,
          887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]


def _primality_test(f):
    for num in range(2, 100):
        result = f(num)
        assert result == (num in primes)

    is_error(ValueError, f, 0)
    is_error(ArithmeticError, f, 1)
    is_error(TypeError, f, "some string")
    is_error(TypeError, f, 1.1)
    is_error(TypeError, f, "some string", 1.1)


def test_primality_test():
    _primality_test(primality_test)


def test_wilsons_theorem():
    _primality_test(wilsons_theorem)


def test_gcd_lcm():
    assert gcd(13, 13) == 13 == abs(13 * 13) // lcm(13, 13)
    assert gcd(-10, 5) == 5 == abs(-10 * 5) // lcm(-10, 5)
    assert gcd(1, 505) == 1 == abs(1 * 505) // lcm(1, 505)

    assert gcd(0, 5) == 5
    assert gcd(5, 0) == 5
    is_error(ArithmeticError, lcm, 0, 5)
    is_error(ArithmeticError, lcm, 0, 0)
    is_error(ArithmeticError, gcd, 0, 0)

    assert gcd(20, 100, 20) == 20
    assert lcm(20, 100, 20) == 100
    assert gcd(-10, -5, -150) == 5
    assert lcm(-10, -5, -150) == 150
    assert gcd(624129, 2061517, 18913) == 18913
    assert lcm(624129, 2061517, 18913) == 68030061

    is_error(TypeError, gcd, 1)
    is_error(TypeError, lcm, 1)


# noinspection PyTypeChecker
def test_digital_root():
    assert digital_root(0) == 0
    assert digital_root(7) == 7
    assert digital_root(10) == 1
    assert digital_root(365) == 5
    assert digital_root(2504152185) == 6

    is_error(ValueError, digital_root, -10)
    is_error(TypeError, digital_root, 3.2)


def test_ackermann_peter():
    assert ackermann_peter(2, 5) == 13
    assert ackermann_peter(0, 5) == 6
    assert ackermann_peter(3, 1) == 13


# noinspection PyTypeChecker
def test_fibonacci():
    assert fibonacci(12) == 144
    assert fibonacci(13, value2=0) == 0
    assert fibonacci(0, value1=2, value2=2) == 2
    assert fibonacci(4, value1=2, value2=2) == 10
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(100) == 354224848179261915075
