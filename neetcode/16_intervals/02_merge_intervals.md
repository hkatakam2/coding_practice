### question
Given an array of intervals where intervals[i] = [start_i, end_i], merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.

You may return the answer in any order.

Note: Intervals are non-overlapping if they have no common point. For example, [1, 2] and [3, 4] are non-overlapping, but [1, 2] and [2, 3] are overlapping.

**1. Restate**
Given list of intervals. Combine overlapping ones. Return list of mutually exclusive intervals covering identical ranges as original input.

**2. Clarify**

* Inputs: List of `[start, end]` integer pairs. Unsorted? Yes.
* Outputs: List of merged `[start, end]` pairs. Any order.
* Assumed: `start <= end` always.
* Overlap definition: touching boundaries overlap (e.g., `[1,2]` and `[2,3]` overlap).
* Constraints: Input can be empty? Yes.

**3. Hand-trace Example**
Input: `[[1,3], [8,10], [2,6], [15,18]]`

* Unsorted is hard to parse. Sort by start time: `[[1,3], [2,6], [8,10], [15,18]]`
* Take first: `[1,3]`.
* Look at next: `[2,6]`. `2` is <= `3`. They overlap. Merge to `[1, max(3,6)]` -> `[1,6]`.
* Look at next: `[8,10]`. `8` is > `6`. No overlap. Keep `[1,6]`, start checking `[8,10]`.
* Look at next: `[15,18]`. `15` is > `10`. No overlap. Keep `[8,10]`, start checking `[15,18]`.
* End of list. Result: `[[1,6], [8,10], [15,18]]`.

**4. Brainstorm & Complexity**

* *Approach A (Brute Force):* Compare every interval to every other interval. If overlap, merge, delete old ones, add new, restart loop. Time: O(N^2). Space: O(N).
* *Approach B (Sort & Sweep):* Sort by start time. Iterate once. Compare current interval to the last merged interval. Same as hand-trace. Time: O(N log N) for sort, O(N) sweep. Space: O(N) for sorting/output.

**5. Suggest Solutions**
Prefer Approach B. Simple, clear. Relies on standard library sort and a single linear pass. Directly mimics the human hand-trace method.

**6. Outline Implementation**

```python
def merge(intervals):
    """
    Reframe: Sorting by start time guarantees overlaps only occur between adjacent intervals in the sweep.
    State: `merged` list, storing confirmed intervals.
    Invariant: Last interval in `merged` always holds maximum end-time of current overlapping group.

    sort_by_start(intervals) = returns intervals ordered by first element.
    get_last(merged) = retrieves the most recently added interval.
    overlaps(a, b) = true if b's start <= a's end.
    extend(a, b) = updates a's end to max(a's end, b's end).

    Core logic:
    - sort intervals by start time
    - add first interval to merged list
    - for each remaining interval in sorted list:
        - get last interval from merged list
        - if current interval overlaps with last:
            - extend last interval
        - else:
            - add current interval to merged list

    Edge cases:
    - empty intervals list
    - one item in intervals list
    """

```

**7. Iterative Implementation**

*Iteration 1: Skeleton with helpers (Happy Path)*

```python
def merge(intervals):
    # sort intervals by start time
    sorted_intervals = sort_by_start(intervals)
    
    merged = []
    # add first interval
    merged.append(sorted_intervals[0]) 
    
    # for each remaining
    for current in sorted_intervals[1:]:
        last = get_last(merged)
        
        if overlaps(last, current):
            extend(last, current)
        else:
            merged.append(current)
            
    return merged

```

*Iteration 2: Inline sorting and basic helpers*

```python
def merge(intervals):
    # CHANGED: standard python sort (sorts by 0th element automatically)
    intervals.sort(key=lambda x: x[0])
    
    merged = []
    merged.append(intervals[0]) 
    
    for current in intervals[1:]:
        # CHANGED: inline get_last
        last = merged[-1]
        
        # CHANGED: inline overlaps logic (current start <= last end)
        if current[0] <= last[1]:
            extend(last, current)
        else:
            merged.append(current)
            
    return merged

```

*Iteration 3: Complete core logic (inline extend)*

```python
def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    
    merged = []
    merged.append(intervals[0]) 
    
    for current in intervals[1:]:
        last = merged[-1]
        
        if current[0] <= last[1]:
            # CHANGED: inline extend (update last end to max of both ends)
            last[1] = max(last[1], current[1])
        else:
            merged.append(current)
            
    return merged

```

*Iteration 4: Patching Edge Cases*
Edge case 1: Empty list. Fails on `intervals[0]`.
Edge case 2: Single item list. Loop doesn't execute, returns item correctly (if it doesn't fail on `intervals[0]`).

```python
def merge(intervals):
    # PATCH: handle empty list edge case
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])
    
    merged = []
    merged.append(intervals[0]) 
    
    for current in intervals[1:]:
        last = merged[-1]
        
        if current[0] <= last[1]:
            last[1] = max(last[1], current[1])
        else:
            merged.append(current)
            
    return merged

```

**8. Complexity & Optimizations**

* **Time Complexity:** `O(N log N)` bottlenecked entirely by the `sort()` function. The linear scan is `O(N)`. Total Time: `O(N log N)`.
* **Space Complexity:** `O(N)` or `O(log N)` depending on the sorting algorithm implementation (Python's Timsort requires `O(N)` auxiliary space). The `merged` array takes `O(N)` space in the worst case (no overlaps).
* **Optimizations:** No asymptotic optimizations exist without changing the problem space (e.g., if inputs were pre-sorted, or if time ranges were tiny integers allowing a boolean array sweep, which they usually aren't). Code is optimally clean. Mutation of `last` object in Python list is fast and requires no array copying.