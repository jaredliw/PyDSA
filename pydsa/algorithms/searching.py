"""Algorithms that are used to check for the presence of an element in an array and retrieve its index.

.. warning:: Some algorithms require the array to be sorted forehead. If :code:`pre_check` is set to False and \
   :code:`arr` is not sorted, an unexpected result will be returned.
"""
from math import sqrt

from pydsa import Any, Iterable, Sequence, NumberSequence, validate_args
from pydsa.algorithms.sorting import is_sorted

__all__ = ["linear_search", "binary_search", "jump_search", "interpolation_search", "exponential_search",
           "ternary_search"]


@validate_args
def linear_search(arr: Iterable, target: Any) -> int:
    """Search sequentially from left to right.

    This algorithm functions well when :paramref:`~pydsa.algorithms.searching.linear_search.arr` is not sorted. It \
    takes :code:`O(n log n)` to sort an array and the efficiencies of other searching algorithms decrease because of \
    this.

    Time complexity: :code:`O(n)`.

    Space complexity: :code:`O(1)`.

    :param arr: An iterable.
    :type arr: Iterable
    :param target: Value to search for.
    :type target: Any
    :returns: Index of :paramref:`~pydsa.algorithms.searching.linear_search.target` in \
    :paramref:`~pydsa.algorithms.searching.linear_search.arr`.
    :rtype: int
    """
    for idx, item in enumerate(arr):
        if item == target:
            return idx
    return -1


@validate_args
def binary_search(arr: Sequence, target: Any, pre_check: bool = True) -> int:
    """Search a sorted array by repeatedly dividing the search interval in half.

    Two prerequisites to use this algorithm:
       * The array must be in sorted order.
       * The array has constant time random access e.g. linked list is not suitable for this algorithm.

    Time complexity: :code:`O(log n)`.

    Space complexity: :code:`O(1)`.

    :param arr: A sequential data structure.
    :type arr: Sequence
    :param target: Value to search for.
    :type target: Any
    :param pre_check: Check :paramref:`~pydsa.algorithms.searching.binary_search.arr` is sorted before running, \
    default to True.
    :type pre_check: bool
    :returns: Index of :paramref:`~pydsa.algorithms.searching.binary_search.target` in \
    :paramref:`~pydsa.algorithms.searching.binary_search.arr`.
    :rtype: int
    :raises ValueError: Raised when :paramref:`~pydsa.algorithms.searching.binary_search.arr` is not sorted and \
    :paramref:`~pydsa.algorithms.searching.binary_search.pre_check` is set to True.
    """

    if pre_check:
        if not is_sorted(arr):
            raise ValueError("this algorithm only works for sorted sequence")

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
    """Search a sorted array by jumping ahead by fixed steps (:math:`\\sqrt{n}` is optimum, where :math:`n` is the \
    length of array).

    This algorithm is less efficient than :func:`~pydsa.algorithms.searching.binary_search`, but it can be used in a \
    system where binary search is costly e.g. in the case that \
    :paramref:`~pydsa.algorithms.searching.jump_search.target` is an extreme value in \
    :paramref:`~pydsa.algorithms.searching.jump_search.arr`.

    Time complexity: :code:`O(sqrt n)`.

    Space complexity: :code:`O(1)`.

    .. note:: **Why the optimal block size is** :math:`\\sqrt{n}` **?** \
    |br| \
    |br| \
    Consider an array with size of :math:`n` and a block size :math:`m`. The worst case is when the value we want \
    to search for is the last element in the array. We need :math:`\\frac{n}{m}+m-1` steps: :math:`\\frac{n}{m}` jumps \
    to reach at the block where the value is located and another :math:`m-1` steps to search linearly in the block. \
    |br| \
    |br| \
    The expression is minimal when the gradient is 0. We differentiate the expression respect to :math:`m`: \
    |jump-search-math-block|

    .. |jump-search-math-block| raw:: html

       <div class="math notranslate nohighlight">
          \\[
             \\begin{split}
                \\frac{\\delta}{\\delta m}(\\frac{n}{m}+m-1) &amp;= 0         \\\\
                                           -\\frac{n}{m^2}+1 &amp;= 0         \\\\
                                              \\frac{n}{m^2} &amp;= 1         \\\\
                                                         m^2 &amp;= n         \\\\
                                                           m &amp;= \\sqrt{n}
             \\end{split}
          \\]
       </div>

    :param arr: A sequential data structure.
    :type arr: Sequence
    :param target: Value to search for.
    :type target: Any
    :param pre_check: Check :paramref:`~pydsa.algorithms.searching.jump_search.arr` is sorted before running, \
    default to True.
    :type pre_check: bool
    :returns: Index of :paramref:`~pydsa.algorithms.searching.jump_search.target` in \
    :paramref:`~pydsa.algorithms.searching.jump_search.arr`.
    :rtype: int
    :raises ValueError: Raised when :paramref:`~pydsa.algorithms.searching.jump_search.arr` is not sorted and \
    :paramref:`~pydsa.algorithms.searching.jump_search.pre_check` is set to True.
    """
    if pre_check:
        if not is_sorted(arr):
            raise ValueError("this algorithm only works for sorted sequence")

    if len(arr) == 0:
        return -1

    optimal_block_size = int(sqrt(len(arr)))
    idx = 0
    for idx in range(0, len(arr), optimal_block_size):
        if arr[idx] == target:
            return idx
        elif idx + optimal_block_size > len(arr) - 1 or arr[idx + optimal_block_size] > target:
            break

    result = linear_search(arr[idx: idx + optimal_block_size], target)
    if result != -1:
        return result + idx
    else:
        return -1


@validate_args
def interpolation_search(arr: NumberSequence, target: Any, pre_check: bool = True) -> int:
    """An improvement over :func:`~pydsa.algorithms.searching.binary_search` for instances, where the values in a \
    sorted array are **uniformly distributed**.

    Time complexity: :code:`O(log log n)`.

    Space complexity: :code:`O(1)`.

    .. note:: **Mechanism behind interpolation search** \
    |br| \
    |br| \
    In :func:`~pydsa.algorithms.searching.binary_search`, we take the average of two pointers i.e. :code:`start` and \
    :code:`end` to find the middle of the array. :func:`~pydsa.algorithms.searching.interpolation_search` improves on \
    this by using the formula: \
    |interpolation-search-formula| \
    The idea of the formula is to return higher value of position when the element to be searched is closer to the end \
    of the array or vice versa. \
    |br| \
    |br| \
    Suppose that we have an array that contains elements that have linear relationship with their indices (the array \
    is said to be uniformly distributed). Therefore, we can construct a formula :math:`f(x)=mx+c` that maps an index \
    to :code:`arr[x]`.\
    |br| \
    |br| \
    Let's say that we have two points i.e. :math:`A=(x_a,f(x_a))` and :math:`B=(x_b,f(x_b))` and we want to find a \
    :math:`x` that maps to :paramref:`~pydsa.algorithms.searching.interpolation_search.target`. (Note: \
    :math:`x_a<x<x_b`) Since three points are lied on the same line, gradient of point :math:`A` and point \
    :math:`(x,f(x))` must be equal to gradient of point :math:`A` and point :math:`B`. thus, an equation can be \
    formed: \
    |interpolation-search-formula-derivation| \
    In most of the real-life cases, we can't form a relationship between indices and elements. However, if it \
    uniformly distributed, graph of :math:`f(x)` will more likely to be a straight line and the formula will be more \
    efficient. \
    |interpolation-formula-external-link|

    .. |interpolation-search-formula| raw:: html

       <div class="math notranslate nohighlight">
          \\[
             \\begin{split}
                pos = start+\\frac{(end-start)\\times(target-arr[start])}{arr[end]-arr[start]}
             \\end{split}
          \\]
       </div>

    .. |interpolation-search-formula-derivation| raw:: html

       <div class="math notranslate nohighlight">
          \\[
             \\begin{split}
                \\frac{f(x_b)-f(x_a)}{x_b-x_a} &amp;= \\frac{f(x)-f(x_a)}{x-x_a}                                 \\\\
                                             x &amp;= x_a + \\frac{(x_b-x_a)\\times(f(x)-f(x_a))}{f(x_b)-f(x_a)}
             \\end{split}
          \\]
       </div>

    .. |interpolation-formula-external-link| raw:: html

       <div class="admonition seealso" style="padding: 2rem 0rem 0rem 0rem;">
          <p class="admonition-title">See also</p>
          <p>
             <a class="reference external" href="https://medium.com/@smellycode/demystifying-interpolation-formula-\
             for-interpolation-search-211780c43269">https://medium.com/@smellycode/demystifying-interpolation-formula-\
             for-interpolation-search-211780c43269</a>
         </p>
       </div>

    :param arr: A sequential data structure.
    :type arr: Sequence
    :param target: Value to search for.
    :type target: Any
    :param pre_check: Check :paramref:`~pydsa.algorithms.searching.interpolation_search.arr` is sorted before running, \
    default to True.
    :type pre_check: bool
    :returns: Index of :paramref:`~pydsa.algorithms.searching.interpolation_search.target` in \
    :paramref:`~pydsa.algorithms.searching.interpolation_search.arr`.
    :rtype: int
    :raises ValueError: Raised when :paramref:`~pydsa.algorithms.searching.interpolation_search.arr` is not sorted and \
    :paramref:`~pydsa.algorithms.searching.interpolation_search.pre_check` is set to True.
    """

    if pre_check:
        if not is_sorted(arr):
            raise ValueError("this algorithm only works for sorted sequence")

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
    """Search exponentially to find the range where :paramref:`~pydsa.algorithms.searching.exponential_search.target` \
    may be present and do :func:`~pydsa.algorithms.searching.binary_search` in the range.

    Time complexity: :code:`O(log n)`.

    Space complexity: :code:`O(1)`.

    :param arr: A sequential data structure.
    :type arr: Sequence
    :param target: Value to search for.
    :type target: Any
    :param pre_check: Check :paramref:`~pydsa.algorithms.searching.exponential_search.arr` is sorted before running, \
    default to True.
    :type pre_check: bool
    :returns: Index of :paramref:`~pydsa.algorithms.searching.exponential_search.target` in \
    :paramref:`~pydsa.algorithms.searching.exponential_search.arr`.
    :rtype: int
    :raises ValueError: Raised when :paramref:`~pydsa.algorithms.searching.exponential_search.arr` is not sorted and \
    :paramref:`~pydsa.algorithms.searching.exponential_search.pre_check` is set to True.
    """
    if pre_check:
        if not is_sorted(arr):
            raise ValueError("this algorithm only works for sorted sequence")

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
    """Similar to :func:`~pydsa.algorithms.searching.binary_search`, this algorithm search a sorted array by \
    repeatedly dividing the search interval into three parts.

    Time complexity: :code:`O(log3 n)`.

    Space complexity: :code:`O(1)`.

    .. note:: :func:`~pydsa.algorithms.searching.ternary_search` **is less preferable over** \
    :func:`~pydsa.algorithms.searching.binary_search` **. Why?** \
    |br| \
    |br| \
    In short, :func:`~pydsa.algorithms.searching.ternary_search` makes more comparisons (means more time is needed!) \
    in worst case. \
    |br| \
    We need at most :math:`4\\lfloor\\log_3 n\\rfloor` comparisons in ternary search but \
    :math:`2\\lfloor\\log_2 n\\rfloor` comparisons in binary search. \
    |br| \
    |binary-ternary-graph| \
    |br| \
    :func:`~pydsa.algorithms.searching.ternary_search` actually adds complexity to the implementation, \
    that's why you seldom use quaternary search or k-nary search for any other higher order.

    .. |binary-ternary-graph| raw:: html

       <div class="align-center figure" id="id1">
          <img alt="alternate text" src="../../../sphinx-source/images/binary-ternary.png">
          <p class="caption"><span class="caption-text">Comparison between the performances
             <a class="reference internal" href="#pydsa.algorithms.searching.binary_search" \
             title="pydsa.algorithms.searching.binary_search">
                <code class="xref py py-func docutils literal notranslate">
                   <span class="pre">binary_search()</span>
                </code>
             </a> and
             <a class="reference internal" href="#pydsa.algorithms.searching.ternary_search" \
             title="pydsa.algorithms.searching.ternary_search">
                <code class="xref py py-func docutils literal notranslate">
                   <span class="pre">ternary_search()</span>
                </code>
             </a>. (For simplicity, floor functions are not plotted)</span>
             <a class="headerlink" href="#id1" title="Permalink to this image">¶</a></p>
       </div>

    :param arr: A sequential data structure.
    :type arr: Sequence
    :param target: Value to search for.
    :type target: Any
    :param pre_check: Check :paramref:`~pydsa.algorithms.searching.exponential_search.arr` is sorted before running, \
    default to True.
    :type pre_check: bool
    :returns: Index of :paramref:`~pydsa.algorithms.searching.exponential_search.target` in \
    :paramref:`~pydsa.algorithms.searching.exponential_search.arr`.
    :rtype: int
    :raises ValueError: Raised when :paramref:`~pydsa.algorithms.searching.ternary_search.arr` is not sorted and \
    :paramref:`~pydsa.algorithms.searching.ternary_search.pre_check` is set to True.
    """
    if pre_check:
        if not is_sorted(arr):
            raise ValueError("this algorithm only works for sorted sequence")

    start = 0
    end = len(arr) - 1

    while start <= end:
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
    return -1
