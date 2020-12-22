from pydsa.algorithms.functions import ackermann_peter


def test_ackermann_peter():
    assert ackermann_peter(2, 5) == 13
    assert ackermann_peter(0, 5) == 6
    assert ackermann_peter(3, 1) == 13
