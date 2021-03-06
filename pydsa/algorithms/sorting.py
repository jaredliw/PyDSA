"""An algorithm that is used to rearrange a given array according to a comparison operator on the elements."""
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
           "slowsort", "stooge_sort", "worstsort", "bogosort", "bogobogosort", "bozosort", "selection_sort",
           "insertion_sort", "merge_sort", "counting_sort", "pigeonhole_sort", "radix_sort", "bucket_sort",
           "bead_sort", "proxmap_sort", "sleep_sort"]


@validate_args
def is_sorted(arr: list, key: Function = lambda x: x, reverse: bool = False) -> bool:
    """Check whether the list is sorted."""

    if reverse:
        cmp_funct = ge
    else:
        cmp_funct = le

    for idx in range(len(arr) - 1):
        if not cmp_funct(key(arr[idx]), key(arr[idx + 1])):
            return False
    return True


def _check_key_arr(arr, key, annot):
    try:
        check_arg("arr", list(map(lambda item: key(item), arr)), annot)
    except ValueError:
        raise ValueError("'arr' is not a(n) '{}' after applying function 'key'".format(annot.__name__))


"""Exchange Sorts"""


@validate_args
def bubble_sort(arr: list, key: Function = lambda x: x, reverse: bool = False) -> list:
    """An algorithm that works by repeatedly swapping the adjacent elements if they are in wrong order."""
    # Time complexity:
    #   Worst (reverse sorted): O(n^2)
    #   Average: Theta(n^2)
    #   Best (sorted): Omega(n)
    # Stable, In place

    if reverse:
        cmp_funct = gt
    else:
        cmp_funct = lt

    arr = deepcopy(arr)
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        # Keep swapping the items if they are larger/smaller than the next item.
        for cur in range(n - i - 1):
            if cmp_funct(key(arr[cur + 1]), key(arr[cur])):
                arr[cur], arr[cur + 1] = arr[cur + 1], arr[cur]
                swapped = True
        # After one inner loop, the largest/smallest item is at the end of the array. In the next loop, we can stop
        # just before it.

        # Optimized Implementation: stopping the algorithm if inner loop did not cause any swap. (Means it is sorted)
        if not swapped:
            break
    return arr


@validate_args
def cocktail_sort(arr: list, key: Function = lambda x: x, reverse: bool = False) -> list:
    """A variation of Bubble Sort. It traverses through a given array in both directions alternatively."""
    # Time complexity:
    #   Worst: O(n^2)
    #   Average: Theta(n^2)
    #   Best (sorted): Omega(n)
    # Stable, In place

    if reverse:
        cmp_funct = gt
    else:
        cmp_funct = lt

    arr = deepcopy(arr)
    n = len(arr)
    for i in range(n - 1):
        swapped = False

        # Forwards
        for cur in range(i, n - i - 1):
            if cmp_funct(key(arr[cur + 1]), key(arr[cur])):
                arr[cur], arr[cur + 1] = arr[cur + 1], arr[cur]
                swapped = True

        # Backwards
        for cur in range(n - i - 1, i, -1):
            if not cmp_funct(key(arr[cur - 1]), key(arr[cur])):
                arr[cur], arr[cur - 1] = arr[cur - 1], arr[cur]
                swapped = True

        if not swapped:
            break

    return arr


@validate_args
def odd_even_sort(arr: list, key: Function = lambda x: x, reverse: bool = False) -> list:
    """A variation of Bubble Sort. The algorithm runs until the array elements are sorted and in each iteration two 
    phases occurs -- Odd and Even Phases."""
    # Time complexity:
    #   Worst (reverse sorted): O(n^2)
    #   Average: Theta(n^2)
    #   Best (sorted): Omega(n)
    # Stable, In place

    if len(arr) <= 1:
        return list(arr)

    if reverse:
        cmp_funct = gt
    else:
        cmp_funct = lt

    arr = deepcopy(arr)
    n = len(arr)
    swapped = True
    while swapped:
        swapped = False

        # Odds
        for cur in range(1, n - 1, 2):
            if cmp_funct(key(arr[cur + 1]), key(arr[cur])):
                arr[cur], arr[cur + 1] = arr[cur + 1], arr[cur]
                swapped = True

        # Evens
        for cur in range(0, n - 1, 2):
            if cmp_funct(key(arr[cur + 1]), key(arr[cur])):
                arr[cur], arr[cur + 1] = arr[cur + 1], arr[cur]
                swapped = True

    return arr


@validate_args
def comb_sort(arr: list, key: Function = lambda x: x, reverse: bool = False) -> list:
    """Improve on Bubble Sort by using gap of size more than 1."""
    # Time complexity:
    #   Worst: O(n^2)
    #   Average: Theta(n^2)
    #   Best: Omega(n^2/2^p), p is a number of increment
    # Stable, In place

    if reverse:
        cmp_funct = gt
    else:
        cmp_funct = lt

    arr = deepcopy(arr)

    # The shrink factor has a great effect on the efficiency of comb sort. k = 1.3 has been suggested as an ideal shrink
    # factor by the authors of the original article after empirical testing on over 200,000 random lists.
    shrink_factor = 1.3
    gap = int(len(arr) // shrink_factor)

    while gap > 1:
        for idx in range(gap):
            idx1 = idx + gap
            if idx1 < len(arr):
                if cmp_funct(key(arr[idx1]), key(arr[idx])):
                    arr[idx], arr[idx1] = arr[idx1], arr[idx]
        gap = int(gap // shrink_factor)

    return bubble_sort(arr, key, reverse)


@validate_args
def gnome_sort(arr: list, key: Function = lambda x: x, reverse: bool = False) -> list:
    """a sorting algorithm which is similar to insertion sort in that it works with one item at a time but gets the item
    to the proper place by a series of swaps, similar to a bubble sort."""
    # Time complexity:
    #   Worst: O(n^2)
    #   Average: Theta(n^2)
    #   Best: Omega(n)
    # Stable, In place

    # Gnome Sort behaves like insertion sort only when it's moving an element into its proper index. Unlike insertion
    # sort, however, gnome sort makes comparisons even after placing an element in its proper spot. If it encounters a
    # value that is out of place, it behaves like insertion sort again.

    if reverse:
        cmp_funct = gt
    else:
        cmp_funct = lt

    arr = deepcopy(arr)
    idx = 1
    # Optimization: Introduce a variable to store the position before traversing back toward the beginning of the list.
    # With this optimization, the gnome sort would become a variant of the insertion sort.
    traversing_back = False
    prev = None
    while idx <= len(arr) - 1:
        if idx > 0 and cmp_funct(key(arr[idx]), key(arr[idx - 1])):
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
def quicksort(arr: list, key: Function = lambda x: x, reverse: bool = False, pivot_funct: Function = None) -> list:
    """A divide-and-conquer algorithm that picks an element as pivot and partitions the given array around the picked
    pivot."""
    # Time complexity:
    #   Worst (always picks greatest or smallest element as pivot): O(n log n)
    #   Average: Theta(n log n)
    #   Best (always picks the middle element as pivot): Omega(n^2)
    # Not stable, In place

    if reverse:
        cmp_funct = gt
    else:
        cmp_funct = lt

    arr = deepcopy(arr)

    def _median_of_three(part):
        if len(part) <= 2:
            return part[0]
        else:
            # Let"s call items[0] as a, items[1] as b and items[2] as c.
            a = part[0]
            b = part[len(part) // 2]
            c = part[-1]

            cmp1 = a < b
            cmp2 = a < c
            cmp3 = b < c

            # Truth table
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
        # Use the default function if the function si not given
        if pivot_funct is None:
            return _median_of_three(part)
        else:
            return pivot_funct(part)

    def _quicksort(part):
        if len(part) <= 1:
            return part
        pivot = _choose_pivot(part)
        pivot_idx = part.index(pivot)
        ptr = 0

        # Move the pivot to the end
        part[pivot_idx], part[-1] = part[-1], part[pivot_idx]

        for idx in range(0, len(part) - 1):
            if cmp_funct(key(part[idx]), key(pivot)):
                part[ptr], part[idx] = part[idx], part[ptr]
                ptr += 1

        # Move pointer back
        part[-1], part[ptr] = part[ptr], part[-1]

        # Sort the partitions
        left = part[:ptr]
        right = part[ptr + 1:]
        return _quicksort(left) + [pivot] + _quicksort(right)

    return _quicksort(arr)


@validate_args
def slowsort(arr: list, key: Function = lambda x: x, reverse: bool = False) -> list:
    """SlowSort is an example of MultiplyAndSurrender - a worst possible sort algorithm. The algorithm decompose the
    problem of sorting n numbers in ascending order into:
        (1) finding the maximum of those numbers, and
        (2) sorting the remaining ones.
    Sub-problem (1) can be further decomposed into
        (1.1) find the maximum of the first n/2 elements,
        (1.2) find the maximum of the remaining n/2 elements, and
        (1.3) find the largest of those two maxima."""

    if reverse:
        cmp_funct = gt
    else:
        cmp_funct = lt

    arr = deepcopy(arr)

    def _slowsort(start=0, end=len(arr) - 1):
        if end <= start:
            return
        # Recursively sort the first half and the second half
        center = (start + end) // 2
        # Step (1.1), the maxima of thr first n/2 elements will be at arr[center].
        _slowsort(start, center)
        # Step (1.2), the maxima of thr first n/2 elements will be at arr[end].
        _slowsort(center + 1, end)

        # Step (1.3), compare maxima and move the largest to the end.
        if cmp_funct(key(arr[end]), key(arr[center])):
            arr[center], arr[end] = arr[end], arr[center]

        # Step (2)
        _slowsort(start, end - 1)

    _slowsort()
    return arr


@validate_args
def stooge_sort(arr: list, key: Function = lambda x: x, reverse: bool = False) -> list:
    """This algorithm divides the array into two overlapping parts (2/3 each). Then it performs sorting in first 2/3
    part and then it performs sorting in last 2/3 part. After that, sorting is done on first 2/3 part to ensure the
    array is sorted."""
    # Time complexity:
    #   Worst: O(n ^ log(3) /log(1.5))
    #   Average: Theta(n ^ log(3) /log(1.5))
    #   Best: Omega(n ^ log(3) /log(1.5))
    # Not stable, In place

    if reverse:
        cmp_funct = gt
    else:
        cmp_funct = lt

    arr = deepcopy(arr)

    def _stooge_sort(start, end):
        if end <= start:
            return
        elif cmp_funct(key(arr[end]), key(arr[start])):
            arr[start], arr[end] = arr[end], arr[start]
        if end - start + 1 > 2:
            # It is important to get the integer sort size used in the recursive calls by rounding the 2/3 upwards, e.g.
            # rounding 2/3 of 5 should give 4 rather than 3, as otherwise the sort can fail on certain data.
            divider = int((end - start + 1) / 3)
            # Sort first 2/3 part of the array
            _stooge_sort(start, end - divider)
            # Sort last 2/3 part of the array
            _stooge_sort(start + divider, end)
            # Sort first 2/3 part of the array again
            _stooge_sort(start, end - divider)
        return

    _stooge_sort(0, len(arr) - 1)
    return arr


@validate_args
def worstsort(arr: list, key: Function = lambda x: x, reverse: bool = False, recursive_depth: NonNegativeInt = 1,
              sorting_algo: Function = bubble_sort) -> list:
    """For k=0, worstsort use bubble sort to sort the array. For any k>0, the algorithm first generates a list of all
    permutations of the array. Then, it use bubble sort to sort the list of permutations and returns the first element
    to worstsort(arr, k-1)."""

    if recursive_depth == 0:
        return bubble_sort(arr, key, reverse)
    else:
        return worstsort(list(sorting_algo(list(permutations(arr)), lambda x: [key(item) for item in x], reverse)[0]),
                         key, reverse, recursive_depth - 1, sorting_algo)  # noqa


@validate_args
def bogosort(arr: list, key: Function = lambda x: x, reverse: bool = False, randomized: bool = False) -> list:
    """An ineffective algorithm based on generate and test paradigm."""
    # Time complexity:
    #   Worst: O(infinity) for randomized version, O((n+1)!) for deterministic version
    #   Average: Theta(n * n!)
    #   Best: Omega(n)
    # Not stable, Not in place (In place for randomized version)

    if randomized:
        while True:
            # Check the order is correct
            if is_sorted(arr, key, reverse):
                break
            shuffle(arr)
    else:
        for perm in permutations(arr):
            perm = list(perm)
            if is_sorted(perm, key, reverse):
                arr = perm
                break
    return arr


@validate_args
def bogobogosort(arr: list, key: Function = lambda x: x, reverse: bool = False, randomized: bool = False) -> list:
    """An algorithm that was designed not to succeed before the heat death of the universe on any sizable list. It works
    by recursively calling itself with smaller and smaller copies of the beginning of the list to see if they are
    sorted."""

    # Time complexity:
    #   Worst: O(infinity) for randomized version, O((n+1)!) for deterministic version
    #   Average: Theta((n +1)!)
    #   Best: Omega(n)
    # Not stable, Not in place (In place for randomized version)

    def _bogobogosort(deck):
        if len(deck) > 1:
            return bogosort(_bogobogosort(deck[:-1]) + [deck[-1]], key, reverse, randomized)
        else:
            return bogosort(deck, key, reverse, randomized)

    return _bogobogosort(arr)


@validate_args
def bozosort(arr: list, key: Function = lambda x: x, reverse: bool = False) -> list:
    """random sorting algorithms where the key idea is to swap any two elements of the list randomly and check if the
    list is sorted."""
    # Time complexity:
    #   Worst: O(infinity)
    #   Average: Theta(n!)
    #   Best: Omega(n)
    # Not stable, In place

    arr = deepcopy(arr)
    end = len(arr) - 1
    while not is_sorted(arr, key, reverse):
        pick1 = randint(0, end)
        pick2 = randint(0, end)
        arr[pick1], arr[pick2] = arr[pick2], arr[pick1]
    return arr


"""Selection Sorts"""


@validate_args
def selection_sort(arr: list, key: Function = lambda x: x, reverse: bool = False) -> list:
    """sorts an array by repeatedly finding the minimum/maximum element from unsorted part and putting it at the
    beginning/end."""
    # Time complexity:
    #   Worst (reverse sorted): O(n^2)
    #   Average: Theta(n^2)
    #   Best (sorted): Omega(n^2)
    # Stable, In place

    arr = deepcopy(arr)
    for ptr in range(len(arr) - 1):
        # Pick the smallest/largest item.
        if reverse:
            idx = max(enumerate(arr[ptr:], ptr), key=lambda x: key(x[1]))[0]
        else:
            idx = min(enumerate(arr[ptr:], ptr), key=lambda x: key(x[1]))[0]

        # Move it to the front.
        arr[ptr], arr[idx] = arr[idx], arr[ptr]
    return arr


"""Insertion Sorts"""


@validate_args
def insertion_sort(arr: list, key: Function = lambda x: x, reverse: bool = False) -> list:
    """An algorithm that works by splitting the array into a sorted and an unsorted part and values from the unsorted
    part are picked and placed at the correct position in the sorted part."""
    # Time complexity:
    #   Worst (reverse sorted): O(n^2)
    #   Average: Theta(n^2)
    #   Best (sorted): Omega(n)
    # Stable, In place

    if reverse:
        cmp_funct = gt
    else:
        cmp_funct = lt

    arr = deepcopy(arr)
    # Items after idx are unsorted, items before idx are sorted.
    for idx, item in enumerate(arr[1:], 1):
        # Find the correct place to insert the new item.
        # Keep moving the items forward (copy the current item to the next item) if it is larger/smaller than the new
        # item than we are inserting now.
        for s_idx, s_item in zip(range(idx - 1, -1, -1), arr[idx - 1::-1]):
            if cmp_funct(key(item), key(s_item)):
                arr[s_idx + 1] = s_item
            else:
                arr[s_idx + 1] = item
                break
        else:
            arr[0] = item
    return arr


"""Merge Sorts"""


@validate_args
def merge_sort(arr: list, key: Function = lambda x: x, reverse: bool = False) -> list:
    """A divide-and-conquer algorithm that divides the input array into two halves, calls itself for the two halves,
    and then merges the two sorted halves."""
    # Time complexity:
    #   Worst: O(n log n)
    #   Average: Theta(n log n)
    #   Best: Omega(n log n)
    # Stable, Not in place

    if reverse:
        cmp_funct = gt
    else:
        cmp_funct = lt

    def _merge_sort(_arr):
        # Break the array into 1 item per partition.
        if len(_arr) <= 1:
            return _arr
        else:
            mid = len(_arr) // 2
            # Merge the partitions two by two
            return _merge(_merge_sort(_arr[:mid]), _merge_sort(_arr[mid:]))

    def _merge(p1, p2):
        ptr1 = 0
        ptr2 = 0
        final = []

        # Compare the items one by one from p1 and p2.
        while ptr1 <= len(p1) - 1 and ptr2 <= len(p2) - 1:
            if cmp_funct(key(p1[ptr1]), key(p2[ptr2])):
                final.append(p1[ptr1])
                ptr1 += 1
            else:
                final.append(p2[ptr2])
                ptr2 += 1

        # Put all the remaining items to final when one pointer reaches the end (means p1 and p2 have the different
        # lengths).
        final.extend(p1[ptr1:])
        final.extend(p2[ptr2:])

        return final

    return _merge_sort(arr)


"""Distribution Sorts"""


# Caution: counting_sort do not support 'key'!
@validate_args
def counting_sort(arr: IntList, reverse: bool = False) -> IntList:
    """Counting sort is a sorting technique based on keys between a specific range. It works by counting the number of
    objects having distinct key values."""
    # Time complexity:
    #   Worst: O(n + k), where k is the range.
    #   Average: Theta(n + k), where k is the range.
    #   Best: Omega(n + k), where k is the range.
    # Not stable, Not in place

    if not arr:
        return []  # noqa

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
    return new  # noqa


@validate_args
def pigeonhole_sort(arr: list, key: Function = lambda x: x, reverse: bool = False,
                    sorting_algo: Function = bubble_sort) -> list:
    """Modified counting sort that sort the range using an underlying algorithm e.g. quicksort. This modified algorithm
     works for any type of elements."""
    # Time complexity:
    #   Worst: O(n + k), where k is the range.
    #   Average: Theta(n + k), where k is the range.
    #   Best: Omega(n + k), where k is the range.
    # Stability depends on sorting_algo, Not in place

    # Difference between Counting Sort and Pigeonhole Sort:
    # Counting Sort counts the occurrence of the items whereas Pigeonhole Sort moves the items into an auxiliary list.

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
        new.extend(sorting_algo(buc, key=key, reverse=reverse))
    return new


@validate_args
def radix_sort(arr: list, key: Function = lambda x: x, reverse: bool = False, order: str = "MSD") -> list:
    """Radix sort is a sorting technique that sorts the elements by first grouping the individual digits of the same
    place value. Then, sort the elements according to their increasing/decreasing order."""
    # Time complexity:
    #   Worst: O(n * k), where k is the range.
    #   Average: Theta(n * k), where k is the range.
    #   Best: Omega(n * k), where k is the range.
    # Not stable, Not in place

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
                "Invalid option '{}', order should be one of the following: {}".format(order, ["LSD", "MSD"]))

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
def bucket_sort(arr: list, key: Function = lambda x: x, reverse: bool = False,
                sorting_algo: Function = insertion_sort) -> list:
    """Bucket sort is a sorting algorithm that works by distributing the elements of an array into a number of buckets.
    Each bucket is then sorted individually, either using a different sorting algorithm, or by recursively applying the
    bucket sorting algorithm."""
    # Time complexity:
    #   Worst: O(n * k), where k is the range.
    #   Average: Theta(n * k), where k is the range.
    #   Best: Omega(n^2)
    # Stable (if sorting_algo is bucket_sort), Not in place

    _check_key_arr(arr, key, IntFloatList)

    def _bucket_sort(part, neg_flag=False):
        if not part:
            return []

        # Optimum number of buckets: ceil(sqrt(n))
        n_of_buckets = ceil(sqrt(len(part)))
        gap = (abs(key(min(part, key=key))) + abs(key(max(part, key=key)))) / n_of_buckets

        buckets = [[] for _ in range(n_of_buckets)]  # Wrong: [[]] * n_of_buckets
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
                    new.extend(sorting_algo(buc, key=key, reverse=reverse))
        return new

    non_negs = _bucket_sort(list(filter(lambda x: key(x) >= 0, arr)))
    negs = _bucket_sort(list(filter(lambda x: key(x) < 0, arr)), neg_flag=True)

    if reverse:
        return non_negs + negs
    else:
        return negs + non_negs


# Caution: bead_sort returns IntList NOT list!
@validate_args
def bead_sort(arr: list, key: Function = lambda x: x, reverse: bool = False) -> IntList:
    """Also known as Gravity sort, this algorithm was inspired from natural phenomena and was designed keeping in mind
     objects(or beads) falling under the influence of gravity."""
    # Time complexity:
    #   Worst: O(S), where S is the sum of the integers.
    #   Average: Theta(S), where S is the sum of the integers.
    #   Best: Omega(S), where S is the sum of the integers.
    # Not stable, Not in place

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
        return poss + zeros + negs  # noqa
    else:
        return negs + zeros + poss  # noqa


@validate_args
def proxmap_sort(arr: list, key: Function = lambda x: x, reverse: bool = False) -> list:
    """Proxmap sort is a sorting algorithm that works by partitioning an array of data items, or keys, into a number of
    "subarrays" (termed buckets, in similar sorts). The name is short for computing a "proximity map," which indicates
    for each key K the beginning of a subarray where K will reside in the final sorted order. Keys are placed into each
    subarray using insertion sort."""
    # Time complexity:
    #   Worst: O(n^2)
    #   Average: Theta(n)
    #   Best: Omega(n)
    # Stable, Not in place

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
def sleep_sort(arr: IntFloatList, key: Function = lambda x: x, reverse: bool = False,
               amplify: [int, float] = 1.0) -> IntFloatList:
    """Work by starting a separate task for each item to be sorted, where each task sleeps for an interval corresponding
     to the item's sort key, then emits the item."""
    # Time complexity:
    #   Worst: O(n + max)
    #   Average: Theta(n + max)
    #   Best: Omega(n + max)
    # Not stable, Not in place, **Not reliable**

    warn("sleep_sort does not guarantee the accuracy of output. Adjust amplify if the output is not as expected.",
         Warning)

    start = False
    final = []

    def _sleep(time):
        # Stuck the thread if not all the threads has started
        while not start:
            pass
        sleep(time * amplify)
        final.append(time)

    # Create threads
    pool = []
    for item in arr:
        t = Thread(target=lambda: _sleep(key(item)))
        pool.append(t)
        t.start()
    start = True

    # Wait until all the threads end before continuing
    for t in pool:
        t.join()

    if reverse:
        return final[::-1]  # noqa
    else:
        return final  # noqa
