### question

You are given two integer arrays nums1 and nums2 of size m and n respectively, where each is sorted in ascending order. Return the median value among all elements of the two arrays.

We need find the **median of two sorted arrays**.

Meaning: imagine merging both arrays into one sorted array, then:

* odd total length → return middle element
* even total length → return average of two middle elements

Example:

```python
nums1 = [1, 3]
nums2 = [2]

merged = [1, 2, 3]
median = 2
```

Another:

```python
nums1 = [1, 2]
nums2 = [3, 4]

merged = [1, 2, 3, 4]
median = (2 + 3) / 2 = 2.5
```

## Clarifying assumptions

I will assume:

* both arrays are sorted ascending
* at least one array is non-empty
* median should be returned as a float when needed

---

# Possible solutions

## Solution 1: Merge then find median

Very straightforward.

```python
nums1 = [1, 2]
nums2 = [3, 4]

merged = [1, 2, 3, 4]
```

Then compute median.

Complexity:

```text
Time:  O(m + n)
Space: O(m + n)
```

We can optimize space by only walking until the middle, but still:

```text
Time: O(m + n)
```

---

## Solution 2: Binary search partition

This is the intended optimal solution.

Instead of fully merging, we split both arrays into:

```text
left half | right half
```

We want:

```text
everything on left <= everything on right
```

Then median comes from the boundary values.

Complexity:

```text
Time:  O(log(min(m, n)))
Space: O(1)
```

---

# Selected implementation: binary search partition

Key idea:

We binary search on the smaller array.

Suppose:

```python
nums1 = [1, 3]
nums2 = [2]
```

Combined length is 3, so left side should contain 2 elements.

A valid partition is:

```text
nums1: [1] | [3]
nums2: [2] | []

left side  = [1, 2]
right side = [3]
```

Largest left value is `2`, so median is `2`.

---

# Implementation outline

```python
def findMedianSortedArrays(nums1, nums2):
    """
    Reframe: Find a partition where left half contains the smaller half
    and all left-side elements are <= all right-side elements.

    State:
    - binary search bounds over the smaller array
    - partition position in nums1
    - matching partition position in nums2
    - four boundary values around the partition

    Invariant:
    - total elements on the left side is always the desired left-half size

    Core logic:
    - always binary search the smaller array
    - choose how many elements nums1 contributes to the left side
    - nums2 contributes the remaining left-side elements
    - inspect the boundary values around both partitions
    - if left side is valid, compute median
    - if nums1 left boundary is too large, move left
    - otherwise move right

    Edge cases:
    - one array is empty
    - total length is odd
    - total length is even
    - partition happens at start of an array
    - partition happens at end of an array
    - arrays have very different sizes
    """
```

---

# Iteration 1: skeleton

```python
def findMedianSortedArrays(nums1, nums2):
    # Make nums1 the smaller array
    if len(nums1) > len(nums2):
        return findMedianSortedArrays(nums2, nums1)

    total = len(nums1) + len(nums2)
    half = (total + 1) // 2

    left = 0
    right = len(nums1)

    while left <= right:
        # choose partition in nums1
        # derive partition in nums2
        # check if partition is valid
        pass
```

---

# Iteration 2: add partition boundaries

When partition is at the edge, we use infinity values.

```python
def findMedianSortedArrays(nums1, nums2):
    if len(nums1) > len(nums2):
        return findMedianSortedArrays(nums2, nums1)

    total = len(nums1) + len(nums2)
    half = (total + 1) // 2

    left = 0
    right = len(nums1)

    while left <= right:
        cut1 = (left + right) // 2
        cut2 = half - cut1

        left1 = float("-inf") if cut1 == 0 else nums1[cut1 - 1]
        right1 = float("inf") if cut1 == len(nums1) else nums1[cut1]

        left2 = float("-inf") if cut2 == 0 else nums2[cut2 - 1]
        right2 = float("inf") if cut2 == len(nums2) else nums2[cut2]

        # partition validation comes next
```

---

# Iteration 3: validate partition

A partition is valid when:

```python
left1 <= right2 and left2 <= right1
```

Why?

Because then every value on the left side is less than or equal to every value on the right side.

```python
def findMedianSortedArrays(nums1, nums2):
    if len(nums1) > len(nums2):
        return findMedianSortedArrays(nums2, nums1)

    total = len(nums1) + len(nums2)
    half = (total + 1) // 2

    left = 0
    right = len(nums1)

    while left <= right:
        cut1 = (left + right) // 2
        cut2 = half - cut1

        left1 = float("-inf") if cut1 == 0 else nums1[cut1 - 1]
        right1 = float("inf") if cut1 == len(nums1) else nums1[cut1]

        left2 = float("-inf") if cut2 == 0 else nums2[cut2 - 1]
        right2 = float("inf") if cut2 == len(nums2) else nums2[cut2]

        if left1 <= right2 and left2 <= right1:
            # compute median here
            pass

        elif left1 > right2:
            right = cut1 - 1

        else:
            left = cut1 + 1
```

---

# Final code

```python
from typing import List


def findMedianSortedArrays(nums1: List[int], nums2: List[int]) -> float:
    """
    Reframe: Find the correct split between left-half and right-half
    without fully merging the arrays.

    State:
    - Binary search range over the smaller array.
    - cut1: how many elements nums1 contributes to the left half.
    - cut2: how many elements nums2 contributes to the left half.
    - Boundary values around both cuts.

    Invariant:
    - The left half always contains exactly half of the combined elements,
      rounded up for odd length.

    Core logic:
    - Binary search the smaller array.
    - Pick a cut in nums1.
    - Compute the matching cut in nums2.
    - Check whether both left boundaries fit before both right boundaries.
    - Once valid, median is determined by boundary values.

    Edge cases:
    - One array is empty.
    - Odd total length.
    - Even total length.
    - Cut is at start of an array.
    - Cut is at end of an array.
    """

    # Always binary search the smaller array.
    if len(nums1) > len(nums2):
        return findMedianSortedArrays(nums2, nums1)

    m = len(nums1)
    n = len(nums2)

    total = m + n
    half = (total + 1) // 2

    left = 0
    right = m

    while left <= right:
        cut1 = (left + right) // 2
        cut2 = half - cut1

        left1 = float("-inf") if cut1 == 0 else nums1[cut1 - 1]
        right1 = float("inf") if cut1 == m else nums1[cut1]

        left2 = float("-inf") if cut2 == 0 else nums2[cut2 - 1]
        right2 = float("inf") if cut2 == n else nums2[cut2]

        # Correct partition found.
        if left1 <= right2 and left2 <= right1:
            # Odd length: median is largest value on left side.
            if total % 2 == 1:
                return float(max(left1, left2))

            # Even length: average of middle two boundary values.
            return (max(left1, left2) + min(right1, right2)) / 2

        # nums1 contributed too many large values to the left side.
        elif left1 > right2:
            right = cut1 - 1

        # nums1 contributed too few values to the left side.
        else:
            left = cut1 + 1

    # This should not happen for valid sorted input.
    raise ValueError("Input arrays are not sorted or invalid.")
```

---

# Complexity

Let:

```text
m = len(nums1)
n = len(nums2)
```

We binary search only the smaller array.

```text
Time:  O(log(min(m, n)))
Space: O(1)
```

The expensive part is only this loop:

```python
while left <= right:
```

Each iteration cuts the search space in half. No merging is done.
