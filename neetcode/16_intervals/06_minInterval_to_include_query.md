### question
You are given a 2D integer array intervals, where intervals[i] = [left_i, right_i] represents the ith interval starting at left_i and ending at right_i (inclusive).

You are also given an integer array of query points queries. The result of query[j] is the length of the shortest interval i such that left_i <= queries[j] <= right_i. If no such interval exists, the result of this query is -1.

Return an array output where output[j] is the result of query[j].

Note: The length of an interval is calculated as right_i - left_i + 1.

## 1. Restate

We have many intervals and many query points.

For each query point, find all intervals that contain that point, then return the **smallest interval length** among them.

Interval is inclusive:

```python
left <= query <= right
```

Length is:

```python
right - left + 1
```

Return answers in the **same order as the original queries**.

---

## 2. Clarifying assumptions

I’ll assume:

1. `intervals` may be unsorted.
2. `queries` may be unsorted and may contain duplicates.
3. Interval endpoints can be any integers.
4. If no interval contains a query, answer is `-1`.

---

## 3. Example by hand

```python
intervals = [[1, 4], [2, 4], [3, 6], [4, 4]]
queries = [2, 3, 4, 5]
```

Interval lengths:

```python
[1, 4] length 4
[2, 4] length 3
[3, 6] length 4
[4, 4] length 1
```

For each query:

```python
query = 2
covered by [1,4], [2,4]
shortest length = 3

query = 3
covered by [1,4], [2,4], [3,6]
shortest length = 3

query = 4
covered by [1,4], [2,4], [3,6], [4,4]
shortest length = 1

query = 5
covered by [3,6]
shortest length = 4
```

Output:

```python
[3, 3, 1, 4]
```

---

## 4. Brainstorm solutions

### Brute force

For every query, check every interval.

```python
for each query:
    scan all intervals
    keep shortest interval that contains query
```

Complexity:

```python
Time: O(number_of_queries * number_of_intervals)
Space: O(1), ignoring output
```

This is simple but too slow for large input.

---

### Better idea: sort + min heap

Key observation:

If we process queries from smallest to largest, we can gradually add intervals whose `left <= query`.

Among active intervals, we want the shortest length. That is exactly what a min heap gives us.

Heap stores:

```python
(interval_length, right_endpoint)
```

Why `right_endpoint`?

Because some intervals started before the current query but already ended before it. Those are expired and must be removed.

For current query:

1. Add all intervals whose start is `<= query`.
2. Remove intervals whose end is `< query`.
3. Heap top is the shortest valid interval covering query.

Need to preserve original query order, so sort queries as:

```python
(query_value, original_index)
```

---

## 5. Selected solution

Use:

```python
sort intervals by left
sort queries by query value, keeping original index
min heap of active intervals
```

This is the standard clean solution.

---

## 6. Implementation outline

```python
def minInterval(intervals, queries):  # -> list[int]
    """
    Reframe: Sweep queries from left to right; at each point, know all intervals
    that could cover it, and use a heap to choose the shortest one.

    State:
        - intervals sorted by start
        - queries sorted by value but carrying original position
        - min heap of active intervals
          Each heap item stores interval length and interval end.
          Chosen because we need fast access to the shortest currently usable interval.

    Invariant:
        Before answering a query, the heap contains intervals that have started.
        After removing expired intervals, heap top is the shortest interval covering the query.

    addStartedIntervals(query) =
        add every interval whose start is not greater than the query.

    removeExpiredIntervals(query) =
        remove intervals whose end is smaller than the query.

    Core logic:
    - Sort intervals by start.
    - Sort query values while remembering where each query originally appeared.
    - Walk through queries from small to large.
    - Add newly available intervals to the heap.
    - Remove intervals that ended before this query.
    - If heap has something, answer is the top interval length.
    - Otherwise answer is -1.
    - Return answers in original query order.

    Edge cases:
    - No intervals.
    - No queries.
    - Query smaller than every interval start.
    - Query larger than every interval end.
    - Query exactly equals interval start or end.
    - Duplicate queries.
    - Multiple intervals with same length.
    - Negative endpoints.
    """
```

---

## 7. Iterative implementation

### Iteration 1: skeleton

```python
import heapq

def minInterval(intervals, queries):
    intervals.sort()
    indexed_queries = sorted((q, i) for i, q in enumerate(queries))

    answers = [-1] * len(queries)
    min_heap = []

    interval_index = 0

    for query, original_index in indexed_queries:
        # add intervals that started
        pass

        # remove intervals that already ended
        pass

        # answer from heap top
        pass

    return answers
```

---

### Iteration 2: add intervals that can start before current query

For every interval with:

```python
left <= query
```

push it into heap.

Heap item:

```python
(length, right)
```

```python
import heapq

def minInterval(intervals, queries):
    intervals.sort()
    indexed_queries = sorted((q, i) for i, q in enumerate(queries))

    answers = [-1] * len(queries)
    min_heap = []

    interval_index = 0

    for query, original_index in indexed_queries:

        # Added: push every interval whose left side is <= current query
        while interval_index < len(intervals) and intervals[interval_index][0] <= query:
            left, right = intervals[interval_index]
            length = right - left + 1
            heapq.heappush(min_heap, (length, right))
            interval_index += 1

        # remove intervals that already ended
        pass

        # answer from heap top
        pass

    return answers
```

---

### Iteration 3: remove expired intervals

An interval is expired when:

```python
right < query
```

Because intervals are inclusive, `right == query` is still valid.

```python
import heapq

def minInterval(intervals, queries):
    intervals.sort()
    indexed_queries = sorted((q, i) for i, q in enumerate(queries))

    answers = [-1] * len(queries)
    min_heap = []

    interval_index = 0

    for query, original_index in indexed_queries:

        while interval_index < len(intervals) and intervals[interval_index][0] <= query:
            left, right = intervals[interval_index]
            length = right - left + 1
            heapq.heappush(min_heap, (length, right))
            interval_index += 1

        # Added: discard intervals that cannot cover current or future queries
        while min_heap and min_heap[0][1] < query:
            heapq.heappop(min_heap)

        # answer from heap top
        pass

    return answers
```

---

### Iteration 4: answer from heap top

If heap is non-empty, shortest valid interval is at heap top.

```python
import heapq

def minInterval(intervals, queries):
    intervals.sort()
    indexed_queries = sorted((q, i) for i, q in enumerate(queries))

    answers = [-1] * len(queries)
    min_heap = []

    interval_index = 0

    for query, original_index in indexed_queries:

        while interval_index < len(intervals) and intervals[interval_index][0] <= query:
            left, right = intervals[interval_index]
            length = right - left + 1
            heapq.heappush(min_heap, (length, right))
            interval_index += 1

        while min_heap and min_heap[0][1] < query:
            heapq.heappop(min_heap)

        # Added: heap top is now the shortest interval covering query
        if min_heap:
            answers[original_index] = min_heap[0][0]

    return answers
```

This is the final core logic.

---

## 8. Edge case walk-through

### Edge case: no intervals

```python
intervals = []
queries = [1, 2, 3]
```

No intervals pushed. Heap always empty.

Output:

```python
[-1, -1, -1]
```

Current code handles it.

---

### Edge case: no queries

```python
intervals = [[1, 3]]
queries = []
```

Loop never runs.

Output:

```python
[]
```

Current code handles it.

---

### Edge case: query exactly at boundary

```python
intervals = [[1, 3]]
queries = [1, 3]
```

Both are inside because inclusive.

Code uses:

```python
left <= query
right < query means expired
```

So `right == query` stays valid.

Current code handles it.

---

### Edge case: duplicate queries

```python
intervals = [[1, 4], [2, 3]]
queries = [2, 2]
```

Both queries keep their own original index.

Current code handles it.

---

## Final code

```python
import heapq
from typing import List

class Solution:
    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        """
        Reframe: Sweep queries from left to right; at each point, the shortest
        active interval is the answer.

        State:
            - intervals sorted by start
            - queries sorted by query value with original index
            - min heap of active intervals as interval length and right endpoint

        Invariant:
            After adding started intervals and removing expired intervals,
            heap top is the shortest interval covering the current query.
        """

        intervals.sort()
        indexed_queries = sorted((query, index) for index, query in enumerate(queries))

        answers = [-1] * len(queries)
        min_heap = []

        interval_index = 0

        for query, original_index in indexed_queries:

            # Add intervals whose left endpoint is <= query.
            while interval_index < len(intervals) and intervals[interval_index][0] <= query:
                left, right = intervals[interval_index]
                length = right - left + 1
                heapq.heappush(min_heap, (length, right))
                interval_index += 1

            # Remove intervals whose right endpoint is < query.
            # They cannot cover current query or any future larger query.
            while min_heap and min_heap[0][1] < query:
                heapq.heappop(min_heap)

            # If heap is non-empty, shortest valid interval is at top.
            if min_heap:
                answers[original_index] = min_heap[0][0]

        return answers
```

## Complexity

Let:

```python
n = len(intervals)
m = len(queries)
```

Sorting:

```python
O(n log n + m log m)
```

Heap work:

Each interval is pushed once and popped at most once.

```python
O(n log n)
```

Total:

```python
Time: O(n log n + m log m)
Space: O(n + m)
```

The expensive section is heap operations. Each active interval operation costs `log n`, but each interval enters and leaves the heap at most once, so this is efficient.
