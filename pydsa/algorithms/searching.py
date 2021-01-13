"""Algorithms that are designed to check for an element or retrieve an element from any data structure where it is
stored."""
from math import sqrt

from pydsa import Any, Sequence, NumberSequence, validate_args
from pydsa.algorithms.sorting import is_sorted

__all__ = ["linear_search", "binary_search", "jump_search", "interpolation_search", "exponential_search",
           "ternary_search"]


@validate_args
def linear_search(arr: Sequence, target: Any) -> int:
    """search an array sequentially from left to right."""
    # Time complexity: O(n)

    for idx, item in enumerate(arr):
        if item == target:
            return idx
    return -1


@validate_args
def binary_search(arr: Sequence, target: Any, pre_check: bool = True) -> int:
    """Search a sorted array by repeatedly dividing the search interval in half."""
    # Time complexity: O(log n)

    if pre_check:
        if not is_sorted(arr):
            raise ValueError("arr is not sorted forehead, this algorithm works for sorted sequence only")

    start = 0
    end = len(arr) - 1
    if end == -1:
        return -1

    mid = start + (end - start) // 2
    while arr[mid] != target:
        if arr[mid] < target:
            start = mid + 1
        else:
            end = mid - 1
        if start > end:
            return -1
        mid = start + (end - start) // 2
    return mid


@validate_args
def jump_search(arr: Sequence, target: Any, pre_check: bool = True) -> int:
    """Search a sorted array by jumping ahead by fixed steps."""
    # Time Complexity: O(sqrt n)

    if pre_check:
        if not is_sorted(arr):
            raise ValueError("arr is not sorted forehead, this algorithm works for sorted sequence only")

    # Less efficient than binary search, but it can be used in a system where binary search is costly. (For example,
    # in the case that the target is the smallest element in the array)

    # Why the optimal block size is sqrt n?
    # https://stackoverflow.com/a/45354833/13080049

    if len(arr) == 0:
        return -1

    optimal_blck_size = int(sqrt(len(arr)))
    idx = 0
    for idx in range(0, len(arr), optimal_blck_size):
        if arr[idx] == target:
            return idx
        elif idx + optimal_blck_size > len(arr) - 1 or arr[idx + optimal_blck_size] > target:
            break

    result = linear_search(arr[idx: idx + optimal_blck_size], target)
    if result != -1:
        return result + idx
    else:
        return -1


@validate_args
def interpolation_search(arr: NumberSequence, target: Any, pre_check: bool = True) -> int:
    """An improvement over Binary Search for instances, where the values in a sorted array are uniformly distributed."""
    # Time complexity: O(log log n)

    if pre_check:
        if not is_sorted(arr):
            raise ValueError("arr is not sorted forehead, this algorithm works for sorted sequence only")

    # Optiimum for arr that are uniformly distributed.

    # Learn more about the interpolation formula:
    # https://medium.com/@smellycode/demystifying-interpolation-formula-for-interpolation-search-211780c43269
    # A small notes: In real cases, the function might not be linear. However, if it is uniformly distributed, the
    # curvature of the graph will be smaller and the formula will be more efficient.

    start = 0
    end = len(arr) - 1
    while start <= end and (arr[start] <= target <= arr[end]):
        if start == end:
            if arr[start] == target:
                return start
            else:
                return end

        pos = int(start + (target - arr[start]) * (end - start) / (arr[end] - arr[start]))
        if arr[pos] == target:
            return pos
        elif arr[pos] < target:
            start = pos + 1
        else:
            end = pos - 1
    return -1


@validate_args
def exponential_search(arr: Sequence, target: Any, pre_check: bool = True) -> int:
    """An algorithm that search exponentially to find the range where element may be present and do binary search in
    the range. """
    # Time complexity: O(log n)

    if pre_check:
        if not is_sorted(arr):
            raise ValueError("arr is not sorted forehead, this algorithm works for sorted sequence only")

    if len(arr) == 0:
        return -1
    elif arr[0] == target:
        return 0

    end = 1
    while end < len(arr) and arr[end] <= target:
        if arr[end] == target:
            return end
        end *= 2
    start = end // 2

    idx = binary_search(arr[start:end], target)
    if idx != -1:
        return start + idx
    else:
        return -1


@validate_args
def ternary_search(arr: Sequence, target: Any, pre_check: bool = True) -> int:
    """Search a sorted array by repeatedly dividing the search interval into three parts."""
    # Time complexity: O(log3 n)

    if pre_check:
        if not is_sorted(arr):
            raise ValueError("arr is not sorted forehead, this algorithm works for sorted sequence only")

    start = 0
    end = len(arr) - 1

    while True:
        if end < start:
            return -1

        divider = (end - start) // 3
        mid1 = start + divider
        mid2 = mid1 + divider

        if arr[mid1] == target:
            return mid1
        elif arr[mid2] == target:
            return mid2
        elif target < arr[mid1]:
            end = mid1 - 1
        elif target > arr[mid2]:
            start = mid2 + 1
        else:
            start = mid1 + 1
            end = mid2 - 1
