### question
Given an unsorted array of integers nums and an integer k, return the kth largest element in the array.

By kth largest element, we mean the kth largest element in the sorted order, not the kth distinct element.

## 1. Restate question

We have an unsorted integer array `nums` and integer `k`.

Return the **kth largest value by position after sorting**, counting duplicates.

Example:

```python
nums = [5, 5, 4, 3]
k = 2
```

Sorted descending:

```python
[5, 5, 4, 3]
```

The 2nd largest is `5`, not `4`, because duplicates count.

---

## 2. Clarifying questions / assumptions

In an interview, I would ask:

1. Is `k` always valid?
   Assume yes: `1 <= k <= len(nums)`.

2. Do duplicates count separately?
   Yes. Problem explicitly says **not kth distinct**.

3. Return value or index?
   Return the value.

---

## 3. Example by hand

```python
nums = [3, 2, 1, 5, 6, 4]
k = 2
```

Sorted descending:

```python
[6, 5, 4, 3, 2, 1]
```

2nd largest = `5`.

Another duplicate example:

```python
nums = [3, 2, 3, 1, 2, 4, 5, 5, 6]
k = 4
```

Sorted descending:

```python
[6, 5, 5, 4, 3, 3, 2, 2, 1]
```

4th largest = `4`.

---

## 4. Brainstorm solutions

### Solution 1: Sort

Sort descending and return index `k - 1`.

```python
nums.sort(reverse=True)
return nums[k - 1]
```

Complexity:

```text
Time: O(n log n)
Space: O(1) or O(n), depending on sorting behavior
```

Very simple, good baseline.

---

### Solution 2: Min heap of size k

Keep only the `k` largest numbers seen so far.

Use a **min heap** because among the current `k` largest numbers, the smallest one is the kth largest candidate.

Example with `k = 2`:

```python
nums = [3, 2, 1, 5, 6, 4]
```

Keep 2 largest seen so far:

```text
see 3 -> [3]
see 2 -> [2, 3]
see 1 -> ignore, smaller than heap min 2
see 5 -> replace 2, keep [3, 5]
see 6 -> replace 3, keep [5, 6]
see 4 -> ignore, smaller than heap min 5
```

At the end, heap has `[5, 6]`.

Smallest among these 2 largest numbers = `5`.

So answer = `5`.

Complexity:

```text
Time: O(n log k)
Space: O(k)
```

This is usually the cleanest interview solution.

---

### Solution 3: Quickselect

Partition like quicksort and search only one side.

Average:

```text
Time: O(n)
Space: O(1) or O(log n)
```

Worst case:

```text
Time: O(n^2)
```

Good optimization, but more implementation-heavy. For interview clarity, I would first present heap.

---

## 5. Selected solution

Use **min heap of size k**.

Key insight:

> The kth largest element is the smallest element among the top k largest elements.

So maintain only top `k`.

---

## 6. Implementation outline first

```python
def findKthLargest(nums: list[int], k: int) -> int:
    """
    Reframe: kth largest is the weakest value among the strongest k values.

    State: min_heap of at most k numbers, chosen because the smallest
        among the kept k largest values is exactly the kth largest.

    Invariant: after processing each number, heap contains the k largest
        numbers seen so far, or all seen numbers if fewer than k seen.

    shouldReplaceCurrentKth(num, heap) = tells whether num is stronger
        than the current kth-largest candidate.

    Core logic:
    - create empty candidate heap
    - walk through every number
    - while fewer than k candidates exist, add the number
    - once k candidates exist:
        - compare current number to weakest candidate
        - if current number is stronger, remove weakest and add current
        - otherwise ignore current number
    - return weakest candidate among the final k candidates

    Edge cases:
    - nums has one element
    - k is one, return max element behavior
    - k equals len(nums), return min element behavior
    - duplicates count as separate values
    - negative numbers still compare normally
    - current number equals heap minimum; ignoring it is safe
    """
```

---

## 7. Iterative implementation

### Iteration 1: skeleton with helper ideas

```python
def findKthLargest(nums, k):
    candidates = create_empty_candidate_heap()

    for num in nums:
        if heap_has_room(candidates, k):
            add_to_candidates(candidates, num)
        elif is_stronger_than_current_kth(num, candidates):
            replace_current_kth(candidates, num)

    return current_kth_largest(candidates)
```

This reads like English.

Now replace helper ideas with actual heap operations.

---

### Iteration 2: import heap tools and create heap

Python’s `heapq` gives a native **min heap**.

```python
import heapq

def findKthLargest(nums, k):
    candidates = []

    for num in nums:
        # still TODO
        pass

    # still TODO
```

---

### Iteration 3: fill heap until size k

```python
import heapq

def findKthLargest(nums, k):
    candidates = []

    for num in nums:
        if len(candidates) < k:
            heapq.heappush(candidates, num)

    # TODO: after heap is full, compare future nums
```

At this point, for the first `k` numbers, we simply add them.

---

### Iteration 4: handle numbers after heap is full

```python
import heapq

def findKthLargest(nums, k):
    candidates = []

    for num in nums:
        if len(candidates) < k:
            heapq.heappush(candidates, num)
        elif num > candidates[0]:
            heapq.heapreplace(candidates, num)

    return candidates[0]
```

Why `candidates[0]`?

Because it is a min heap. The smallest among the kept `k` largest values is at the root.

That root is the kth largest element.

---

## Final code

```python
from typing import List
import heapq


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        """
        Reframe: kth largest is the weakest value among the strongest k values.

        State: min_heap of at most k numbers, chosen because the smallest
            among the kept k largest values is exactly the kth largest.

        Invariant: after processing each number, heap contains the k largest
            numbers seen so far, or all seen numbers if fewer than k seen.

        Core logic:
        - create empty candidate heap
        - walk through every number
        - while fewer than k candidates exist, add the number
        - once k candidates exist:
            - compare current number to weakest candidate
            - if current number is stronger, remove weakest and add current
            - otherwise ignore current number
        - return weakest candidate among the final k candidates

        Edge cases:
        - nums has one element
        - k is one
        - k equals len(nums)
        - duplicates count separately
        - negative numbers compare normally
        - equal-to-root values do not change the answer
        """

        candidates = []

        for num in nums:
            if len(candidates) < k:
                heapq.heappush(candidates, num)
            elif num > candidates[0]:
                heapq.heapreplace(candidates, num)

        return candidates[0]
```

---

## 8. Walk edge cases after core logic

### Edge case 1: one element

```python
nums = [7]
k = 1
```

Heap becomes:

```python
[7]
```

Return `7`.

Works.

---

### Edge case 2: `k = 1`

```python
nums = [3, 2, 5, 1]
k = 1
```

Heap keeps only the biggest seen so far.

```text
3 -> [3]
2 -> ignore
5 -> replace 3
1 -> ignore
```

Return `5`.

Works.

---

### Edge case 3: `k = len(nums)`

```python
nums = [3, 2, 5, 1]
k = 4
```

Heap keeps all numbers.

Smallest in heap = `1`.

The 4th largest is indeed `1`.

Works.

---

### Edge case 4: duplicates

```python
nums = [5, 5, 4, 3]
k = 2
```

Heap can keep both `5`s.

Return `5`.

Works because duplicates are pushed as separate values.

---

### Edge case 5: negative numbers

```python
nums = [-1, -5, -3]
k = 2
```

Sorted descending:

```python
[-1, -3, -5]
```

2nd largest = `-3`.

Heap comparisons still work normally.

---

## Complexity

The expensive operation is heap insertion/replacement.

Heap size never grows beyond `k`.

Each heap operation costs:

```text
O(log k)
```

We process `n` numbers.

Final complexity:

```text
Time: O(n log k)
Space: O(k)
```

Sorting would be simpler but slower for small `k`:

```text
Sorting: O(n log n)
Heap:    O(n log k)
```
