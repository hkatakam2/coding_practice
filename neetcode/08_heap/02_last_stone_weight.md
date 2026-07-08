### question
You are given an array of integers stones where stones[i] represents the weight of the ith stone.

We want to run a simulation on the stones as follows:

At each step we choose the two heaviest stones, with weight x and y and smash them togethers
If x == y, both stones are destroyed
If x < y, the stone of weight x is destroyed, and the stone of weight y has new weight y - x.
Continue the simulation until there is no more than one stone remaining.

Return the weight of the last remaining stone or return 0 if none remain.

## 1. Restate the problem

We have stone weights. Repeatedly:

1. Pick the two heaviest stones.
2. Smash them.
3. If same weight, both disappear.
4. If different, the heavier stone remains with reduced weight: `heavier - lighter`.
5. Continue until zero or one stone remains.

Return the last stone weight, or `0` if no stones remain.

---

## 2. Clarifying questions / assumptions

In an interview I would confirm:

* Can `stones` be empty? Usually yes possible, return `0`.
* Are weights positive integers? Usually yes.
* Duplicates allowed? Yes.
* We only need final weight, not the simulation history.
* We should optimize repeated “get two largest” operation.

---

## 3. Example by hand

Input:

```python
stones = [2, 7, 4, 1, 8, 1]
```

Two heaviest each time:

```text
[2, 7, 4, 1, 8, 1]

pick 8 and 7
8 - 7 = 1
remaining: [2, 4, 1, 1, 1]

pick 4 and 2
4 - 2 = 2
remaining: [2, 1, 1, 1]

pick 2 and 1
2 - 1 = 1
remaining: [1, 1, 1]

pick 1 and 1
equal, both destroyed
remaining: [1]

answer = 1
```

---

## 4. Brainstorm solutions

### Solution 1: Sort every time

At every step:

```text
sort stones
take last two
insert difference if needed
```

Easy to understand, but expensive.

Complexity:

```text
There can be O(n) smash operations.
Each sort costs O(n log n).
Total: O(n^2 log n)
```

---

### Solution 2: Max heap

We repeatedly need the two largest stones.

That is exactly what a max heap gives us.

Python only has a min heap, so we store negative weights:

```text
stone 8 becomes -8
stone 7 becomes -7
```

The smallest negative number represents the largest original value.

Example:

```python
stones = [2, 7, 4, 1, 8, 1]
heap = [-8, -7, -4, -1, -2, -1]
```

Then:

```python
heaviest = -heapq.heappop(heap)
second_heaviest = -heapq.heappop(heap)
```

Complexity:

```text
Build heap: O(n)
Each smash: O(log n)
At most n - 1 smashes
Total: O(n log n)
Space: O(n)
```

This is the preferred interview solution.

---

## 5. Selected solution

Use a max heap simulated with negative numbers.

---

## 6. Implementation outline

```python
def lastStoneWeight(stones):  # -> int
    """
    Reframe: repeatedly remove the two largest values; a heap is the clean DS.

    State: max_heap, implemented as negative values in Python's min heap,
        chosen because we need efficient access to the current heaviest stones.

    Invariant: before each smash, the heap contains all stones still remaining,
        represented as negative weights.

    buildMaxHeap(stones) = convert stone weights into negative weights and heapify.
    popHeaviest(heap) = remove and return the largest original stone weight.
    addStone(heap, weight) = insert a remaining stone weight if it is positive.

    Core logic:
    - put every stone into a max heap
    - while at least two stones remain:
        - remove the heaviest stone
        - remove the second heaviest stone
        - if they are different:
            - put back the leftover weight
    - if one stone remains, return it
    - otherwise return zero

    Edge cases:
    - no stones
    - one stone
    - two equal stones
    - two unequal stones
    - many duplicate stones
    - all stones eventually destroyed
    """
```

---

## 7. Iterative implementation

### Iteration 1: skeleton

```python
import heapq
from typing import List

def lastStoneWeight(stones: List[int]) -> int:
    max_heap = build_max_heap(stones)

    while has_at_least_two_stones(max_heap):
        first = pop_heaviest(max_heap)
        second = pop_heaviest(max_heap)

        if first != second:
            leftover = first - second
            add_stone(max_heap, leftover)

    return final_answer(max_heap)
```

This reads clearly, but helpers are not implemented yet.

---

### Iteration 2: implement heap helpers

```python
import heapq
from typing import List

def build_max_heap(stones: List[int]) -> List[int]:
    # Python heapq is min heap, so store negative weights
    heap = [-stone for stone in stones]
    heapq.heapify(heap)
    return heap

def has_at_least_two_stones(heap: List[int]) -> bool:
    return len(heap) >= 2

def pop_heaviest(heap: List[int]) -> int:
    # Convert negative heap value back to positive stone weight
    return -heapq.heappop(heap)

def add_stone(heap: List[int], weight: int) -> None:
    heapq.heappush(heap, -weight)

def final_answer(heap: List[int]) -> int:
    if heap:
        return -heap[0]
    return 0
```

---

### Iteration 3: full working version with helpers

```python
import heapq
from typing import List

def lastStoneWeight(stones: List[int]) -> int:
    max_heap = build_max_heap(stones)

    while has_at_least_two_stones(max_heap):
        first = pop_heaviest(max_heap)
        second = pop_heaviest(max_heap)

        if first != second:
            leftover = first - second
            add_stone(max_heap, leftover)

    return final_answer(max_heap)


def build_max_heap(stones: List[int]) -> List[int]:
    heap = [-stone for stone in stones]
    heapq.heapify(heap)
    return heap


def has_at_least_two_stones(heap: List[int]) -> bool:
    return len(heap) >= 2


def pop_heaviest(heap: List[int]) -> int:
    return -heapq.heappop(heap)


def add_stone(heap: List[int], weight: int) -> None:
    heapq.heappush(heap, -weight)


def final_answer(heap: List[int]) -> int:
    if heap:
        return -heap[0]
    return 0
```

This is very readable, but in interviews we usually inline small helpers.

---

### Iteration 4: final interview version

```python
import heapq
from typing import List

def lastStoneWeight(stones: List[int]) -> int:
    # Convert to negative numbers to simulate max heap
    heap = [-stone for stone in stones]
    heapq.heapify(heap)

    while len(heap) >= 2:
        first = -heapq.heappop(heap)
        second = -heapq.heappop(heap)

        if first != second:
            leftover = first - second
            heapq.heappush(heap, -leftover)

    if heap:
        return -heap[0]

    return 0
```

---

## 8. Edge case walkthrough

### Empty input

```python
stones = []
```

Heap is empty.

Loop does not run.

Returns:

```python
0
```

---

### One stone

```python
stones = [5]
```

Heap has one stone.

Loop does not run.

Returns:

```python
5
```

---

### Two equal stones

```python
stones = [4, 4]
```

Pop:

```text
4 and 4
```

Same weight, both destroyed.

Heap empty.

Returns:

```python
0
```

---

### Two unequal stones

```python
stones = [10, 4]
```

Pop:

```text
10 and 4
```

Push:

```text
6
```

Returns:

```python
6
```

---

### Many duplicates

```python
stones = [3, 3, 3]
```

Process:

```text
3 and 3 destroyed
left [3]
```

Returns:

```python
3
```

---

## 9. Complexity

Let `n` be the number of stones.

Heap construction:

```text
O(n)
```

Each smash operation does:

```text
2 heap pops + maybe 1 heap push
```

Each heap operation costs:

```text
O(log n)
```

There are at most `n - 1` smash rounds.

Final complexity:

```text
Time: O(n log n)
Space: O(n)
```

Final answer:

```python
import heapq
from typing import List

def lastStoneWeight(stones: List[int]) -> int:
    heap = [-stone for stone in stones]
    heapq.heapify(heap)

    while len(heap) >= 2:
        first = -heapq.heappop(heap)
        second = -heapq.heappop(heap)

        if first != second:
            heapq.heappush(heap, -(first - second))

    return -heap[0] if heap else 0
```

Yes — correct. In **Python 3.14+**, `heapq` has native max-heap helpers:

```python
heapq.heapify_max(heap)
heapq.heappop_max(heap)
heapq.heappush_max(heap, item)
heapq.heappushpop_max(heap, item)
heapq.heapreplace_max(heap, item)
```

These were added in Python 3.14. The official docs now say `heapq` supports both `heapify()` for min-heaps and `heapify_max()` for max-heaps, with the max-heap API using the `_max` suffix. ([Python documentation][1])

So in Python 3.14+, the cleaner version is:

```python
import heapq
from typing import List

def lastStoneWeight(stones: List[int]) -> int:
    heapq.heapify_max(stones)

    while len(stones) >= 2:
        first = heapq.heappop_max(stones)
        second = heapq.heappop_max(stones)

        if first != second:
            heapq.heappush_max(stones, first - second)

    return stones[0] if stones else 0
```

But for interviews, I would still mention both:

```text
If Python 3.14+ is available, use heapq max-heap APIs.
Otherwise, use the common negative-value trick because many platforms still run older Python versions.
```

For LeetCode-style environments, the negative-value version is still safer unless you know the Python runtime is 3.14+.

[1]: https://docs.python.org/3/library/heapq.html?utm_source=chatgpt.com "heapq — Heap queue algorithm"
