"""Sorting algorithms are used to rearrange a given array according to a comparison operator on the elements."""
from copy import deepcopy
from itertools import permutations
from math import ceil, sqrt
from operator import le, lt, ge, gt
from random import randint, shuffle
from threading import Thread
from time import sleep
from warnings import warn

from pydsa import check_arg, Function, IntList, NonNegativeInt, IntFloatList, validate_args

__all__ = ["is_sorted", "bubble_sort", "cocktail_sort", "odd_even_sort", "comb_sort", "gnome_sort", "quicksort",
           "slowsort", "heap_sort", "stooge_sort", "worstsort", "bogosort", "bogobogosort", "bozosort",
           "selection_sort", "insertion_sort", "merge_sort", "counting_sort", "pigeonhole_sort", "radix_sort",
           "bucket_sort", "bead_sort", "proxmap_sort", "sleep_sort"]


@validate_args
def is_sorted(arr: list, /, *, key: Function = lambda x: x, reverse: bool = False) -> bool:
    """Check whether the list is sorted."""

    if reverse:
        cmp = ge
    else:
        cmp = le

    for idx in range(len(arr) - 1):
        if not cmp(key(arr[idx]), key(arr[idx + 1])):
            return False
    return True


def _check_key_arr(arr, key, annot):
    try:
        check_arg("arr", list(map(lambda item: key(item), arr)), annot)
    except ValueError:
        raise ValueError("'arr' is not a(n) '{}' after applying function 'key'.".format(annot.__name__))


"""Exchange Sorts"""


@validate_args
def bubble_sort(arr: list, /, *, key: Function = lambda x: x, reverse: bool = False) -> list:
    """Sort by repeatedly swapping the adjacent elements if they are in wrong order."""
    # Time complexity:
    #   Worst (reverse sorted): O(n^2)
    #   Average: Theta(n^2)
    #   Best (sorted): Omega(n)
    # Stable. In place.

    if reverse:
        cmp = gt
    else:
        cmp = lt

    arr = deepcopy(arr)
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        # Keep swapping the items if they are in wrong order.
        for cur in range(n - i - 1):
            if cmp(key(arr[cur + 1]), key(arr[cur])):
                arr[cur], arr[cur + 1] = arr[cur + 1], arr[cur]
                swapped = True
        # After one pass, the largest item is in the right place. So, we can stop right before it.

        # Optimization: If no swap is made, we are done.
        if not swapped:
            break
    return arr


@validate_args
def cocktail_sort(arr: list, /, *, key: Function = lambda x: x, reverse: bool = False) -> list:
    """A variation of Bubble Sort, sort by traversing through a given array in both directions alternatively."""
    # Time complexity:
    #   Worst: O(n^2)
    #   Average: Theta(n^2)
    #   Best (sorted): Omega(n)
    # Stable. In place.

    if reverse:
        cmp = gt
    else:
        cmp = lt

    arr = deepcopy(arr)

    n = len(arr)
    for i in range(n - 1):
        swapped = False

        # Forwards.
        for cur in range(i, n - i - 1):
            if cmp(key(arr[cur + 1]), key(arr[cur])):
                arr[cur], arr[cur + 1] = arr[cur + 1], arr[cur]
                swapped = True

        # Backwards.
        for cur in range(n - i - 1, i, -1):
            if not cmp(key(arr[cur - 1]), key(arr[cur])):
                arr[cur], arr[cur - 1] = arr[cur - 1], arr[cur]
                swapped = True

        if not swapped:
            break

    return arr


@validate_args
def odd_even_sort(arr: list, /, *, key: Function = lambda x: x, reverse: bool = False) -> list:
    """A variation of Bubble Sort. The algorithm runs until the array elements are sorted and in each iteration two
    phases occurs -- odd and even phases."""
    # Time complexity:
    #   Worst (reverse sorted): O(n^2)
    #   Average: Theta(n^2)
    #   Best (sorted): Omega(n)
    # Stable. In place.

    if reverse:
        cmp = gt
    else:
        cmp = lt

    arr = deepcopy(arr)

    def _phrase(*, even):
        for cur in range(0 if even else 1, n - 1, 2):
            if cmp(key(arr[cur + 1]), key(arr[cur])):
                arr[cur], arr[cur + 1] = arr[cur + 1], arr[cur]
                nonlocal swapped
                swapped = True

    n = len(arr)
    if n > 1:
        swapped = True
        while swapped:
            swapped = False
            _phrase(even=False)
            _phrase(even=True)
    return arr


@validate_args
def comb_sort(arr: list, /, *, key: Function = lambda x: x, reverse: bool = False) -> list:
    """Improve on Bubble sort by using gap of size more than 1."""
    # Time complexity:
    #   Worst: O(n^2)
    #   Average: Theta(n^2)
    #   Best: Omega(n^2/2^p), p is the number of increment
    # Stable. In place.

    if reverse:
        cmp = gt
    else:
        cmp = lt

    arr = deepcopy(arr)

    # The shrink factor has a great effect on the efficiency of comb sort. `k` = 1.3 is known to be an ideal shrink
    # factor after empirical testing on over 200,000 random lists.
    shrink_factor = 1.3
    gap = int(len(arr) // shrink_factor)

    while gap > 1:
        for idx in range(gap):
            idx1 = idx + gap
            if idx1 < len(arr) and cmp(key(arr[idx1]), key(arr[idx])):
                arr[idx], arr[idx1] = arr[idx1], arr[idx]
        gap = int(gap // shrink_factor)

    return bubble_sort(arr, key=key, reverse=reverse)


@validate_args
def gnome_sort(arr: list, /, *, key: Function = lambda x: x, reverse: bool = False) -> list:
    # noinspection GrazieInspection
    """Similar to Insertion sort in that it works with one item at a time but gets the item to the proper place by a
    series of swaps."""
    # Time complexity:
    #   Worst: O(n^2)
    #   Average: Theta(n^2)
    #   Best: Omega(n)
    # Stable. In place.

    # Gnome sort behaves like insertion sort only when it is moving an element into its proper index. Unlike insertion
    # sort, however, gnome sort makes comparisons even after placing an element in its proper spot. If it encounters a
    # value that is out of place, it behaves like insertion sort again.

    if reverse:
        cmp = gt
    else:
        cmp = lt

    arr = deepcopy(arr)
    idx = 1
    traversing_back = False
    prev = None
    while idx <= len(arr) - 1:
        if idx > 0 and cmp(key(arr[idx]), key(arr[idx - 1])):
            arr[idx - 1], arr[idx] = arr[idx], arr[idx - 1]
            idx -= 1
            if not traversing_back:
                prev = idx
            traversing_back = True
        else:
            if traversing_back:
                idx = prev
                traversing_back = False
            idx += 1

    return arr


@validate_args
def quicksort(arr: list, /, *, key: Function = lambda x: x, reverse: bool = False,
              pivot_choosing_algorithm: Function = None) -> list:
    """Sort by picking an element as pivot and partitions the given array around the picked pivot
    (divide-and-conquer).
    Pivot choosing algorithm is a function that takes an array and returns a pivot. If it is not provided,
    median-of-three algorithm is used."""
    # Time complexity:
    #   Worst (always picks greatest or smallest element as pivot): O(n log n)
    #   Average: Theta(n log n)
    #   Best (always picks the middle element as pivot): Omega(n^2)
    # Not stable. In place.

    if reverse:
        cmp = gt
    else:
        cmp = lt

    arr = deepcopy(arr)

    def _median_of_three(part):
        if len(part) <= 2:
            return part[0]
        else:
            a = part[0]
            b = part[len(part) // 2]
            c = part[-1]

            cmp1 = a < b
            cmp2 = a < c
            cmp3 = b < c

            # Truth table:
            # a < b  T  T  T  T  F  F  F  F
            # a < c  T  T  F  F  T  T  F  F
            # b < c  T  F  T  F  T  F  T  F
            #        b  c  -  a  a  -  c  b

            s = sum([cmp1, cmp2, cmp3])
            if s == 3 or s == 0:
                return b
            elif s == 2:
                if not cmp3:
                    return c
                else:
                    return a
            else:
                if cmp1:
                    return a
                else:
                    return c

    def _choose_pivot(part):
        # Use the default function if it is not provided.
        if pivot_choosing_algorithm is None:
            return _median_of_three(part)
        else:
            return pivot_choosing_algorithm(part)

    def _quicksort(part):
        if len(part) <= 1:
            return part
        pivot = _choose_pivot(part)
        pivot_idx = part.index(pivot)
        ptr = 0

        # Move the pivot to the end.
        part[pivot_idx], part[-1] = part[-1], part[pivot_idx]

        for idx in range(0, len(part) - 1):
            if cmp(key(part[idx]), key(pivot)):
                part[ptr], part[idx] = part[idx], part[ptr]
                ptr += 1

        # Move pointer back to its original position.
        part[-1], part[ptr] = part[ptr], part[-1]

        # Sort the partitions.
        left = part[:ptr]
        right = part[ptr + 1:]
        return _quicksort(left) + [pivot] + _quicksort(right)

    return _quicksort(arr)


@validate_args
def slowsort(arr: list, /, *, key: Function = lambda x: x, reverse: bool = False) -> list:
    """SlowSort is an example of MultiplyAndSurrender -- the worst possible sort algorithm. The algorithm decompose the
    problem of sorting n numbers in ascending order into:
    1. Finding the maximum of those numbers, and
    2. Sorting the remaining ones.

    Sub-problem 1 can be further decomposed into:
    1.1 find the maximum of the first n/2 elements, and
    1.2 find the maximum of the remaining n/2 elements, and
    1.3 find the largest of those two maxima.
    """
    # Time complexity:
    #   Worst: O(n^log n)
    #   Average: Theta(n^log n)
    #   Best: Omega(n^log n)
    # Stable. In place.

    if reverse:
        cmp = gt
    else:
        cmp = lt

    arr = deepcopy(arr)

    def _slowsort(start=0, end=len(arr) - 1):
        if end <= start:
            return
        # Recursively sort the first half, and the second half.
        center = (start + end) // 2
        # Step (1.1), the maxima of the first n/2 elements will be at `arr[center]`.
        _slowsort(start, center)
        # Step (1.2), the maxima of the first n/2 elements will be at `arr[end]`.
        _slowsort(center + 1, end)

        # Step (1.3), compare maxima and move the largest to the end.
        if cmp(key(arr[end]), key(arr[center])):
            arr[center], arr[end] = arr[end], arr[center]

        # Step (2)
        _slowsort(start, end - 1)

    _slowsort()
    return arr


@validate_args
def heap_sort(arr: list, /, *, key: Function = lambda x: x, reverse: bool = False) -> list:
    """Heap-based, sort by building a heap from the array, then repeatedly extracting the maximum element from the heap
    and inserting it into the sorted array."""
    # Time complexity:
    #   Worst: O(n log n)
    #   Average: Theta(n log n)
    #   Best: Omega(n log n)
    # Not stable. In place.

    if reverse:
        cmp = gt
    else:
        cmp = lt

    arr = deepcopy(arr)

    def _heapify(idx):
        left_child_idx = 2 * idx + 1
        right_child_idx = left_child_idx + 1

        idx_max_or_min = idx
        if left_child_idx < heap_size and not cmp(key(arr[left_child_idx]), key(arr[idx_max_or_min])):
            idx_max_or_min = left_child_idx
        if right_child_idx < heap_size and not cmp(key(arr[right_child_idx]), key(arr[idx_max_or_min])):
            idx_max_or_min = right_child_idx

        if idx_max_or_min != idx:
            arr[idx], arr[idx_max_or_min] = arr[idx_max_or_min], arr[idx]
            _heapify(idx_max_or_min)

    # Build heap.
    heap_size = len(arr)
    for i in range(heap_size // 2, -1, -1):
        # Heapify every node, except leaves (since they do not have children).
        _heapify(i)
    # Sort.
    for i in range(heap_size - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heap_size -= 1
        # Heapify root node.
        _heapify(0)
    return arr


@validate_args
def stooge_sort(arr: list, /, *, key: Function = lambda x: x, reverse: bool = False) -> list:
    """Sort by dividing the array into two overlapping parts (2/3 each). Then it performs sorting in the first 2/3
    parts, and then it performs sorting in the last 2/3 part. After that, sorting is done again on the first 2/3 part
    to ensure the array is sorted."""
    # Time complexity:
    #   Worst: O(n ^ log(3) /log(1.5))
    #   Average: Theta(n ^ log(3) /log(1.5))
    #   Best: Omega(n ^ log(3) /log(1.5))
    # Not stable. In place.

    if reverse:
        cmp = gt
    else:
        cmp = lt

    arr = deepcopy(arr)

    def _stooge_sort(start, end):
        if end <= start:
            return
        elif cmp(key(arr[end]), key(arr[start])):
            arr[start], arr[end] = arr[end], arr[start]
        if end - start + 1 > 2:
            divider = int((end - start + 1) / 3)
            # Sort first 2/3 part of the array
            _stooge_sort(start, end - divider)
            # Sort last 2/3 part of the array
            _stooge_sort(start + divider, end)
            # Sort first 2/3 part of the array again
            _stooge_sort(start, end - divider)

    _stooge_sort(0, len(arr) - 1)
    return arr


@validate_args
def worstsort(arr: list, /, *, key: Function = lambda x: x, reverse: bool = False, recursion_depth: NonNegativeInt = 1,
              sorting_algorithm: Function = bubble_sort) -> list:
    """For `k` equals to 0, Worstsort use Bubble sort to sort the array. Otherwise, the algorithm first generates a
    list of all permutations of the array. Then, it uses Bubble sort to sort the list of permutations and returns the
    first element to `worstsort(arr, k-1)`."""
    # Time complexity:
    #   Worst: O(n ^ k)
    #   Average: Theta(n ^ k)
    #   Best: Omega(n ^ k)
    # Stability depends on `sorting_algorithm`. Not in place.

    if recursion_depth == 0:
        return bubble_sort(arr, key=key, reverse=reverse)
    else:
        # noinspection PyTypeChecker
        return worstsort(
            list(sorting_algorithm(
                list(permutations(arr)),
                key=lambda x: [key(item) for item in x],
                reverse=reverse
            )[0]),
            key=key, reverse=reverse, recursion_depth=recursion_depth - 1,
            sorting_algorithm=sorting_algorithm)


@validate_args
def bogosort(arr: list, /, *, key: Function = lambda x: x, reverse: bool = False, randomized: bool = False) -> list:
    """Sort by randomly swapping elements in the array, and hoping that it will eventually sort itself. Another way of
    implementation is to check all the permutations of the array until we find a sorted one."""
    # Time complexity:
    #   Worst: O(infinity) if `randomized` is `True`, O((n+1)!) otherwise
    #   Average: Theta(n * n!)
    #   Best: Omega(n)
    # Not stable. In place if `randomized` is `True`.

    if randomized:
        while True:
            if is_sorted(arr, key=key, reverse=reverse):
                break
            shuffle(arr)
    else:
        for perm in permutations(arr):
            perm = list(perm)
            if is_sorted(perm, key=key, reverse=reverse):
                arr = perm
                break
    return arr


@validate_args
def bogobogosort(arr: list, /, *, key: Function = lambda x: x, reverse: bool = False, randomized: bool = False) -> list:
    """Sort by recursively calling itself with smaller and smaller copies of the beginning of the list to see if they
    are sorted. (An algorithm that was designed not to succeed before the heat death of the universe on any sizable
    list.)"""
    # Time complexity:
    #   Worst: O(infinity) when `randomized` is `True`, O((n+1)!) otherwise
    #   Average: Theta((n +1)!)
    #   Best: Omega(n)
    # Not stable. In place if `randomized` is `True`.

    def _bogobogosort(deck):
        if len(deck) > 1:
            return bogosort(_bogobogosort(deck[:-1]) + [deck[-1]], key=key, reverse=reverse, randomized=randomized)
        else:
            return bogosort(deck, key=key, reverse=reverse, randomized=randomized)

    return _bogobogosort(arr)


@validate_args
def bozosort(arr: list, /, *, key: Function = lambda x: x, reverse: bool = False) -> list:
    """Sort by randomly swapping any two elements of the list and checking if the list is sorted."""
    # Time complexity:
    #   Worst: O(infinity)
    #   Average: Theta(n!)
    #   Best: Omega(n)
    # Not stable. In place.

    arr = deepcopy(arr)
    end = len(arr) - 1
    while not is_sorted(arr, key=key, reverse=reverse):
        pick1 = randint(0, end)
        pick2 = randint(0, end)
        arr[pick1], arr[pick2] = arr[pick2], arr[pick1]
    return arr


"""Selection Sorts"""


@validate_args
def selection_sort(arr: list, /, *, key: Function = lambda x: x, reverse: bool = False) -> list:
    """Sort by repeatedly finding the minimum/maximum element from unsorted part and move it to the front."""
    # Time complexity:
    #   Worst (reverse sorted): O(n^2)
    #   Average: Theta(n^2)
    #   Best (sorted): Omega(n^2)
    # Stable. In place.

    if reverse:
        cmp = max
    else:
        cmp = min

    arr = deepcopy(arr)
    for ptr in range(len(arr) - 1):
        # Pick the smallest/largest item.
        idx = cmp(enumerate(arr[ptr:], ptr), key=lambda x: key(x[1]))[0]

        # Move it to the front.
        arr[ptr], arr[idx] = arr[idx], arr[ptr]
    return arr


"""Insertion Sorts"""


@validate_args
def insertion_sort(arr: list, /, *, key: Function = lambda x: x, reverse: bool = False) -> list:
    """Sort by splitting the array into a sorted and an unsorted part, and values from the unsorted part are picked and
    placed at the correct position in the sorted part."""
    # Time complexity:
    #   Worst (reverse sorted): O(n^2)
    #   Average: Theta(n^2)
    #   Best (sorted): Omega(n)
    # Stable. In place.

    if reverse:
        cmp = gt
    else:
        cmp = lt

    arr = deepcopy(arr)

    # Items after `idx` are unsorted, items before `idx` are sorted.
    for idx, item in enumerate(arr[1:], 1):
        # Find the correct place to insert the new item.
        # Keep moving the items forward (copy the current item to the next item) if it is larger/smaller than the item
        # we are inserting now.
        for s_idx, s_item in zip(range(idx - 1, -1, -1), arr[idx - 1::-1]):
            if cmp(key(item), key(s_item)):
                arr[s_idx + 1] = s_item
            else:
                arr[s_idx + 1] = item
                break
        else:
            arr[0] = item
    return arr


"""Merge Sorts"""


@validate_args
def merge_sort(arr: list, /, *, key: Function = lambda x: x, reverse: bool = False) -> list:
    """Sort by dividing the array into two halves (divide-and-conquer), calling itself for the two halves, and then
    merging the two sorted halves."""
    # Time complexity:
    #   Worst: O(n log n)
    #   Average: Theta(n log n)
    #   Best: Omega(n log n)
    # Stable. Not in place.

    if reverse:
        cmp = gt
    else:
        cmp = lt

    def _merge_sort(_arr):
        # Partition the array until it is the only element in the subarray.
        if len(_arr) <= 1:
            return _arr
        else:
            mid = len(_arr) // 2
            # Merge partitions.
            return _merge(_merge_sort(_arr[:mid]), _merge_sort(_arr[mid:]))

    def _merge(p1, p2):
        ptr1 = 0
        ptr2 = 0
        final = []

        # Compare every item in `p1` with `p2`.
        while ptr1 <= len(p1) - 1 and ptr2 <= len(p2) - 1:
            if cmp(key(p1[ptr1]), key(p2[ptr2])):
                final.append(p1[ptr1])
                ptr1 += 1
            else:
                final.append(p2[ptr2])
                ptr2 += 1

        # Put all the remaining items to `final` when one pointer reaches the end.
        final.extend(p1[ptr1:])
        final.extend(p2[ptr2:])

        return final

    return _merge_sort(arr)


"""Distribution Sorts"""


@validate_args
def counting_sort(arr: IntList, /, *, reverse: bool = False) -> IntList:
    """Sort by counting the number of objects having distinct key values."""
    # Time complexity:
    #   Worst: O(n + k), where k is the range.
    #   Average: Theta(n + k), where k is the range.
    #   Best: Omega(n + k), where k is the range.
    # Not stable. Not in place.

    # **This sorting algorithm does not support 'key'.**

    if not arr:
        # noinspection PyTypeChecker
        return []

    _min = min(arr)
    _max = max(arr)

    count_arr = list(0 for _ in range(_min, _max + 1))
    for item in arr:
        count_arr[item - _min] += 1

    if reverse:
        step = -1
    else:
        step = 1
    new = []
    for idx, occur in enumerate(count_arr[::step]):
        if reverse:
            new.extend([(_max - idx)] * occur)
        else:
            new.extend([(_min + idx)] * occur)
    # noinspection PyTypeChecker
    return new


@validate_args
def pigeonhole_sort(arr: list, /, *, key: Function = lambda x: x, reverse: bool = False,
                    sorting_algorithm: Function = bubble_sort) -> list:
    """Modified counting sort that sorts the range using an underlying algorithm, e.g., quicksort. This modified
    algorithm works for any type of elements."""
    # Time complexity:
    #   Worst: O(n + k), where k is the range.
    #   Average: Theta(n + k), where k is the range.
    #   Best: Omega(n + k), where k is the range.
    # Stability depends on `sorting_algorithm`. Not in place.

    # Difference between Counting sort and Pigeonhole sort:
    # Counting sort counts the occurrence of the items, whereas Pigeonhole sort moves the items into an auxiliary list.

    if not arr:
        return []

    _check_key_arr(arr, key, IntList)
    _min = key(min(arr, key=key))
    _max = key(max(arr, key=key))

    count_arr = list([] for _ in range(_min, _max + 1))
    for item in arr:
        count_arr[key(item) - _min].append(item)

    if reverse:
        step = -1
    else:
        step = 1
    new = []
    for buc in count_arr[::step]:
        new.extend(sorting_algorithm(buc, key=key, reverse=reverse))
    return new


@validate_args
def radix_sort(arr: list, /, *, key: Function = lambda x: x, reverse: bool = False, order: str = "MSD") -> list:
    """Sort by grouping the individual digits of the same place value. Then, sort the elements according to their
    increasing/decreasing order."""
    # Time complexity:
    #   Worst: O(n * k), where k is the range.
    #   Average: Theta(n * k), where k is the range.
    #   Best: Omega(n * k), where k is the range.
    # Not stable. Not in place.

    _check_key_arr(arr, key, IntList)

    def _radix_sort(part, n_digit=None):
        if not part:
            return []

        new = []
        if n_digit is None:
            n_digit = len(str(key(max(part, key=lambda x: abs(key(x))))).lstrip("-"))
        if order == "LSD":
            bound = n_digit
            n_digit = 0
        elif order == "MSD":
            bound = 1
        else:
            raise ValueError(
                "Invalid option '{}', order should be one of the following: {}.".format(order, ["LSD", "MSD"]))

        buckets = [[] for _ in range(10)]
        for item in part:
            idx = int(abs(key(item)) // (10 ** (n_digit - 1)) % 10)
            if reverse:
                idx = 9 - idx
            buckets[idx].append(item)

        for buc in buckets:
            if buc:
                if len(buc) == 1 or n_digit == bound:
                    new.extend(buc)
                else:
                    new.extend(_radix_sort(buc, n_digit - 1))
        return new

    non_negs = _radix_sort(list(filter(lambda x: key(x) >= 0, arr)))

    reverse = not reverse
    negs = _radix_sort(list(filter(lambda x: key(x) < 0, arr)))
    reverse = not reverse

    if reverse:
        return non_negs + negs
    else:
        return negs + non_negs


@validate_args
def bucket_sort(arr: list, /, *, key: Function = lambda x: x, reverse: bool = False,
                sorting_algorithm: Function = insertion_sort) -> list:
    """Sort by distributing the elements of an array into several buckets. Each bucket is then sorted individually,
        either using a different sorting algorithm, or by recursively applying Bucket sort."""
    # Time complexity:
    #   Worst: O(nk), where k is the range.
    #   Average: Theta(nk), where k is the range.
    #   Best: Omega(n^2)
    # Stable (if `sorting_algorithm` is `bucket_sort()`). Not in place.

    _check_key_arr(arr, key, IntFloatList)

    def _bucket_sort(part, neg_flag=False):
        if not part:
            return []

        # The optimal number of buckets: ceil(sqrt(n)).
        n_of_buckets = ceil(sqrt(len(part)))
        gap = (abs(key(min(part, key=key))) + abs(key(max(part, key=key)))) / n_of_buckets

        # Wrong: `buckets = [[]] * n_of_buckets`.
        buckets = [[] for _ in range(n_of_buckets)]
        for item in part:
            idx = int(abs(key(item)) // gap)
            if idx < 0:
                idx = 0
            elif idx > n_of_buckets - 1:
                idx = n_of_buckets - 1
            if reverse ^ neg_flag:
                idx = n_of_buckets - idx - 1
            buckets[idx].append(item)

        new = []
        for buc in buckets:
            if buc:
                if len(buc) == 1:
                    new.extend(buc)
                else:
                    new.extend(sorting_algorithm(buc, key=key, reverse=reverse))
        return new

    non_negs = _bucket_sort(list(filter(lambda x: key(x) >= 0, arr)))
    negs = _bucket_sort(list(filter(lambda x: key(x) < 0, arr)), neg_flag=True)

    if reverse:
        return non_negs + negs
    else:
        return negs + non_negs


@validate_args
def bead_sort(arr: list, /, *, key: Function = lambda x: x, reverse: bool = False) -> IntList:
    """Also known as Gravity sort, this algorithm was inspired from natural phenomena and was designed keeping in mind
     objects (or beads) falling under the influence of gravity."""
    # Time complexity:
    #   Worst: O(S), where S is the sum of the integers.
    #   Average: Theta(S), where S is the sum of the integers.
    #   Best: Omega(S), where S is the sum of the integers.
    # Not stable. Not in place.

    # **This sorting algorithm returns `IntList`, not list.**

    _check_key_arr(arr, key, IntList)

    def _bead_sort(part, neg_flag=False):
        if not part:
            return []

        _max = abs(key(max(part, key=lambda x: abs(key(x)))))
        poles = [0] * _max
        for num in part:
            for i in range(abs(key(num))):
                poles[i] += 1

        new = []
        while poles:
            total = 0
            for idx, p in enumerate(poles):
                if p == 0:
                    poles.pop(idx)
                else:
                    total += 1
                    poles[idx] -= 1
            if total == 0:
                break
            if neg_flag:
                new.append(-1 * total)
            else:
                new.append(total)

        if (not reverse) ^ neg_flag:
            return new[::-1]
        else:
            return new

    poss = _bead_sort(list(filter(lambda x: key(x) > 0, arr)))
    zeros = list(filter(lambda x: key(x) == 0, arr))
    negs = _bead_sort(list(filter(lambda x: key(x) < 0, arr)), neg_flag=True)

    if reverse:
        # noinspection PyTypeChecker
        return poss + zeros + negs
    else:
        # noinspection PyTypeChecker
        return negs + zeros + poss


@validate_args
def proxmap_sort(arr: list, /, *, key: Function = lambda x: x, reverse: bool = False) -> list:
    # noinspection GrazieInspection
    """Sort by partitioning an array of data items, or keys, into several buckets. The name is short for computing a
    'proximity map' which indicates for each key K the beginning of a subarray where K will reside in the final
    sorted order. Keys are placed into each subarray using Insertion sort."""
    # Time complexity:
    #   Worst: O(n^2)
    #   Average: Theta(n)
    #   Best: Omega(n)
    # Stable. Not in place.

    _check_key_arr(arr, key, IntFloatList)

    if not arr:
        return []

    _min = key(min(arr, key=key))
    _max = key(max(arr, key=key))

    hit_counts = [0 for _ in range(int(_min), int(_max + 1))]
    for item in arr:
        hit_counts[int(key(item)) - int(_min)] += 1

    proxmaps = []
    last_hit_count = 0
    for hc in hit_counts:
        if hc == 0:
            proxmaps.append(None)
        else:
            proxmaps.append(last_hit_count)
            last_hit_count += hc

    locations = []
    for item in arr:
        locations.append(proxmaps[int(key(item)) - int(_min)])

    final = [None for _ in range(len(locations))]
    for idx, item in enumerate(arr):
        loc = locations[idx]
        if final[loc] is None:
            final[loc] = item
        else:
            none_ptr = loc
            while final[none_ptr] is not None:
                none_ptr += 1
            for ptr in range(none_ptr - 1, loc - 1, -1):
                if final[ptr] > item:
                    final[ptr], final[ptr + 1] = final[ptr + 1], final[ptr]
                else:
                    final[ptr + 1] = item
                    break
            else:
                final[loc] = item

    if reverse:
        final = final[::-1]
    return final


"""Miscellaneous"""


@validate_args
def sleep_sort(arr: IntFloatList, /, *, key: Function = lambda x: x, reverse: bool = False,
               amplify: [int, float] = 1.0) -> IntFloatList:
    """Sort by starting a separate task for each item to be sorted, where each task sleeps for an interval
    corresponding to the item's sort key, then emits the item."""
    # Time complexity:
    #   Worst: O(n + max)
    #   Average: Theta(n + max)
    #   Best: Omega(n + max)
    # Not stable. Not in place. **Unreliable**.

    # noinspection GrazieInspection
    warn("`sleep_sort()` does not guarantee the accuracy of the output, adjust `amplify` accordingly.", Warning)

    start = False
    final = []

    def _sleep(time):
        # Wait until all the threads start.
        while True:
            if start:
                sleep(time * amplify)
                final.append(time)
                break

    # Create threads.
    pool = []
    for item in arr:
        t = Thread(target=lambda x=item: _sleep(key(x)))
        pool.append(t)
        t.start()
    start = True

    # Wait until all the threads end.
    for t in pool:
        t.join()

    if reverse:
        # noinspection PyTypeChecker
        return final[::-1]
    else:
        # noinspection PyTypeChecker
        return final
