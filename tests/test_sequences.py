from pydsa.algorithms.sequences import fibonacci


def test_fibonacci():
    assert fibonacci(12) == 144
    assert fibonacci(13, value2=0) == 0
    assert fibonacci(0, value1=2, value2=2) == 2
    assert fibonacci(4, value1=2, value2=2) == 10
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(100) == 354224848179261915075
