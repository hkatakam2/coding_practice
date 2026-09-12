### question
Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return **the median** of the two sorted arrays.

The overall run time complexity should be `O(log (m+n))`.

**Example 1:**

```
Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
Explanation: merged array = [1,2,3] and median is 2.

```

**Example 2:**

```
Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.
```

Assume Python, arrays sorted ascending, at least one array non-empty. I’d handle this in an interview like this.

## 1. Restate

We have two individually sorted arrays.

Need median of all `m + n` values **without actually merging everything**, because merging costs `O(m+n)`.

Target:

```text
Time: O(log(m+n))
```

We need effectively find the middle value(s) of the conceptual merged array.

---

# 2. Clarifying questions

I would ask interviewer:

* arrays sorted ascending? → yes
* duplicates allowed? → assume yes
* negative numbers allowed? → yes
* can one array be empty? → assume yes
* can both arrays be empty? → normally LeetCode guarantees total length >= 1
* expected floating-point median? → yes
* allowed to use `±infinity` sentinels? → yes

---

# 3. Example by hand

### Example

```text
nums1 = [1, 3]
nums2 = [2]
```

Conceptually:

```text
[1, 2, 3]
```

We need split the combined values into two halves:

```text
left  = [1]
right = [2, 3]
```

Median:

```text
min(right) = 2
```

But instead of physically merging, can we find where to cut each original array?

Put smaller array first:

```text
A = [2]
B = [1, 3]
```

Try partition:

```text
A:        | 2
B:      1 | 3

left side = [1]
right side = [2, 3]
```

Boundary values:

```text
Aleft  = -∞
Aright = 2

Bleft  = 1
Bright = 3
```

For this to be a valid partition:

```text
Aleft <= Bright
Bleft <= Aright
```

which is:

```text
-∞ <= 3
1 <= 2
```

true.

Total size odd, so median is:

```text
min(Aright, Bright)
= min(2, 3)
= 2
```

---

# 4. Brainstorm possible solutions

## Solution 1: Merge arrays

Same thing we did by hand.

```text
nums1 = [1,3]
nums2 = [2]

merge -> [1,2,3]
take middle
```

Two pointers.

```python
def findMedianSortedArrays(nums1, nums2):
    merged = []

    i = j = 0

    while i < len(nums1) and j < len(nums2):
        if nums1[i] <= nums2[j]:
            merged.append(nums1[i])
            i += 1
        else:
            merged.append(nums2[j])
            j += 1

    merged.extend(nums1[i:])
    merged.extend(nums2[j:])

    n = len(merged)

    if n % 2:
        return float(merged[n // 2])

    return (merged[n // 2 - 1] + merged[n // 2]) / 2
```

Complexity:

```text
Time  O(m+n)
Space O(m+n)
```

Correct, easy, but violates required complexity.

---

## Solution 2: Find kth element

Instead of merging, repeatedly discard roughly half of one array.

Median is:

```text
odd:
k = total // 2

even:
k1 = total // 2 - 1
k2 = total // 2
```

Can find kth smallest in logarithmic time.

Valid solution.

But bookkeeping around indices and repeatedly finding two middle elements makes implementation slightly less clean.

---

## Solution 3: Binary search partition

Key observation:

Median only cares about dividing combined values into:

```text
LEFT HALF | RIGHT HALF
```

such that:

```text
every value on left <= every value on right
```

Since both arrays are already sorted, we only need to choose:

```text
where to partition nums1
where to partition nums2
```

If we choose the partition in one array, the other partition is automatically determined because left side must contain a fixed number of values.

Binary search that partition.

```text
Time: O(log(min(m,n)))
Space: O(1)
```

This is even stronger than required `O(log(m+n))`.

I would choose this.

---

# 5. Derive the partition solution

Say:

```text
A = nums1
B = nums2
```

Always binary-search the smaller array.

Suppose combined length is:

```text
total = m + n
```

Number of values we want on the left:

```text
half = (total + 1) // 2
```

The `+1` conveniently makes the left side contain the median when total length is odd.

Suppose we take `i` values from `A`.

Then we must take:

```text
j = half - i
```

values from `B`.

Visually:

```text
A:  ... Aleft | Aright ...
                 ^
                 i

B:  ... Bleft | Bright ...
                 ^
                 j
```

We have correct partition when:

```text
Aleft <= Bright
AND
Bleft <= Aright
```

Why?

Because inside each array things are already sorted.

So these two boundary checks guarantee:

```text
everything left <= everything right
```

---

## What if partition is wrong?

Suppose:

```text
Aleft > Bright
```

Example:

```text
A: 1  8 | 10
B: 2    | 3  9
```

`8 > 3`.

We took too many values from `A`.

Move partition in `A` left.

---

Suppose:

```text
Bleft > Aright
```

Example:

```text
A: 1 | 2  10
B: 3 | 4  9
```

`3 > 2`.

We didn't take enough values from `A`.

Move partition in `A` right.

That's our binary search.

---

# 6. Implementation outline

```python
def findMedianSortedArrays(nums1, nums2):  # -> float
    """
    Reframe:
    Find a partition of both sorted arrays where the combined left half
    contains the correct number of elements and every left value <= every
    right value.

    State:
    Binary-search bounds over the smaller array, chosen because picking
    its partition uniquely determines the partition of the other array.

    Invariant:
    The two partitions together always place exactly `half` elements on
    the left side.


    getBoundaryValues(partition):
        return values immediately left and right of both partitions.


    Core logic:
    - make A the smaller array
    - compute how many elements belong in the combined left half
    - binary-search how many elements should come from A
    - derive how many must come from B
    - inspect only the four values surrounding the two partitions
    - if both left boundary values are <= opposite right boundary values:
        partition is valid
    - if A contributes too-large a value to the left:
        move A's partition left
    - otherwise:
        move A's partition right
    - once valid:
        odd total -> smallest value on right / equivalent left convention
        even total -> average largest left and smallest right

    Edge cases:
    - one array empty
    - partition before first element of an array
    - partition after last element of an array
    - odd total length
    - even total length
    - duplicate values
    - negative values
    - one array much larger than the other
    """
```

One detail: because we're using

```python
half = (total + 1) // 2
```

for **odd length**, median will actually be:

```text
max(Aleft, Bleft)
```

because left side contains the extra element.

This convention makes code cleaner.

---

# 7. Iterative implementation

## Iteration 1 — skeleton

Start with plain flow.

```python
def findMedianSortedArrays(nums1, nums2):
    A = nums1
    B = nums2

    # make A smaller

    # determine combined left-half size

    # binary-search partition of A
    while True:
        # choose A partition

        # derive B partition

        # get four boundary values

        if partition_is_valid:
            # calculate median
            pass

        elif too_many_from_A:
            # move left
            pass

        else:
            # move right
            pass
```

---

## Iteration 2 — smaller array + binary search

```python
def findMedianSortedArrays(nums1, nums2):
    A = nums1
    B = nums2

    # Added: binary-search only the smaller array.
    if len(A) > len(B):
        A, B = B, A

    total = len(A) + len(B)

    # Added: number of elements belonging to left partition.
    half = (total + 1) // 2

    left = 0
    right = len(A)

    while left <= right:
        # Added: choose how many elements A contributes.
        i = (left + right) // 2

        # Added: B contributes the remainder.
        j = half - i

        # TODO boundary values
        # TODO validate partition
```

Important interview distinction:

`i` means:

```text
number of A elements on left
```

not necessarily "array index of median".

Same for `j`.

---

## Iteration 3 — get boundary values

Normal partition:

```text
A = [1, 3, 7, 9]

take i = 2

[1, 3] | [7, 9]

Aleft = 3
Aright = 7
```

So:

```python
Aleft = A[i - 1]
Aright = A[i]
```

Same for B.

Add:

```python
def findMedianSortedArrays(nums1, nums2):
    A = nums1
    B = nums2

    if len(A) > len(B):
        A, B = B, A

    total = len(A) + len(B)
    half = (total + 1) // 2

    left = 0
    right = len(A)

    while left <= right:
        i = (left + right) // 2
        j = half - i

        # Added: values immediately around both partitions.
        Aleft = A[i - 1]
        Aright = A[i]

        Bleft = B[j - 1]
        Bright = B[j]

        # TODO validate partition
```

This core logic now works only when partitions are strictly inside both arrays.

We'll patch boundaries after core logic.

---

## Iteration 4 — partition validation

Correct partition:

```text
Aleft <= Bright
Bleft <= Aright
```

Add that.

```python
def findMedianSortedArrays(nums1, nums2):
    A = nums1
    B = nums2

    if len(A) > len(B):
        A, B = B, A

    total = len(A) + len(B)
    half = (total + 1) // 2

    left = 0
    right = len(A)

    while left <= right:
        i = (left + right) // 2
        j = half - i

        Aleft = A[i - 1]
        Aright = A[i]

        Bleft = B[j - 1]
        Bright = B[j]

        # Added: found the correct combined partition.
        if Aleft <= Bright and Bleft <= Aright:
            # TODO median
            pass

        # Added: too many large values from A are on the left.
        elif Aleft > Bright:
            right = i - 1

        # Added: not enough values from A are on the left.
        else:
            left = i + 1
```

---

## Iteration 5 — calculate median

For odd total:

```text
left half contains one extra element
```

So:

```python
median = max(Aleft, Bleft)
```

For even total:

```text
largest left = max(Aleft, Bleft)
smallest right = min(Aright, Bright)
```

Therefore:

```python
median = (largest_left + smallest_right) / 2
```

Core logic:

```python
def findMedianSortedArrays(nums1, nums2):
    A = nums1
    B = nums2

    if len(A) > len(B):
        A, B = B, A

    total = len(A) + len(B)
    half = (total + 1) // 2

    left = 0
    right = len(A)

    while left <= right:
        i = (left + right) // 2
        j = half - i

        Aleft = A[i - 1]
        Aright = A[i]

        Bleft = B[j - 1]
        Bright = B[j]

        if Aleft <= Bright and Bleft <= Aright:

            # Added: odd combined length.
            if total % 2 == 1:
                return float(max(Aleft, Bleft))

            # Added: even combined length.
            return (
                max(Aleft, Bleft) +
                min(Aright, Bright)
            ) / 2

        elif Aleft > Bright:
            right = i - 1

        else:
            left = i + 1
```

Happy-path algorithm complete.

Now patch edge cases.

---

# 8. Edge cases

## Edge case 1: partition before first element

Could have:

```text
i = 0

A:
| 1 2 3
```

There is no `Aleft`.

Logically, nothing from A exists on the left.

We want it to never violate:

```text
Aleft <= Bright
```

Therefore pretend:

```text
Aleft = -∞
```

Patch:

```python
Aleft = A[i - 1] if i > 0 else float("-inf")
```

---

## Edge case 2: partition after last element

Could have:

```text
A:
1 2 3 |
```

There is no `Aright`.

Pretend:

```text
Aright = +∞
```

Patch:

```python
Aright = A[i] if i < len(A) else float("inf")
```

Do same thing for B.

Now:

```python
Aleft = A[i - 1] if i > 0 else float("-inf")
Aright = A[i] if i < len(A) else float("inf")

Bleft = B[j - 1] if j > 0 else float("-inf")
Bright = B[j] if j < len(B) else float("inf")
```

This also handles an empty array naturally.

---

# Final implementation

```python
class Solution:
    def findMedianSortedArrays(
        self,
        nums1: list[int],
        nums2: list[int]
    ) -> float:

        # Binary-search the smaller array.
        A, B = nums1, nums2

        if len(A) > len(B):
            A, B = B, A

        total = len(A) + len(B)
        half = (total + 1) // 2

        left = 0
        right = len(A)

        while left <= right:
            # Number of elements contributed to the left half.
            i = (left + right) // 2
            j = half - i

            # Values surrounding both partitions.
            Aleft = A[i - 1] if i > 0 else float("-inf")
            Aright = A[i] if i < len(A) else float("inf")

            Bleft = B[j - 1] if j > 0 else float("-inf")
            Bright = B[j] if j < len(B) else float("inf")

            # Correct partition.
            if Aleft <= Bright and Bleft <= Aright:

                if total % 2 == 1:
                    return float(max(Aleft, Bleft))

                return (
                    max(Aleft, Bleft)
                    + min(Aright, Bright)
                ) / 2

            # Too many elements taken from A.
            elif Aleft > Bright:
                right = i - 1

            # Too few elements taken from A.
            else:
                left = i + 1
```

# Walk Example 2

```text
nums1 = [1,2]
nums2 = [3,4]
```

`A` already smaller/equal.

```text
total = 4
half = 2

left = 0
right = 2
```

First partition:

```text
i = 1
j = 1

A: 1 | 2
B: 3 | 4

Aleft  = 1
Aright = 2
Bleft  = 3
Bright = 4
```

Check:

```text
1 <= 4      yes
3 <= 2      no
```

Need more from A:

```text
left = 2
```

Next:

```text
i = 2
j = 0

A: 1 2 |
B:     | 3 4

Aleft  = 2
Aright = +∞

Bleft  = -∞
Bright = 3
```

Valid:

```text
2 <= 3
-∞ <= +∞
```

Even length:

```text
largest left  = max(2, -∞) = 2
smallest right = min(+∞, 3) = 3

median = (2 + 3) / 2
       = 2.5
```

# Complexity

We binary-search only the smaller array.

If:

```text
m = len(nums1)
n = len(nums2)
```

then:

```text
Time:  O(log(min(m, n)))
Space: O(1)
```

`O(log(min(m,n)))` satisfies the requested `O(log(m+n))`.

### Interview one-line insight

> "Instead of finding the median directly, I binary-search for a partition of the two arrays such that the combined left half contains the correct number of elements and every left-side value is less than or equal to every right-side value."
