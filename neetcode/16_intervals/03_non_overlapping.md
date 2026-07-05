### question
Given an array of intervals intervals where intervals[i] = [start_i, end_i], return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.

Note: Intervals are non-overlapping even if they have a common point. For example, [1, 3] and [2, 4] are overlapping, but [1, 2] and [2, 3] are non-overlapping.

**1. Restating**
Goal: Find minimum intervals to remove to eliminate all overlaps.
Touching endpoints (e.g., [1,2] and [2,3]) do not count as overlaps.

**2. Clarifying**

* Input: Unsorted array of `[start, end]` pairs? (Yes)
* Output: Integer representing removals? (Yes)
* Data bounds: Negative coordinates possible? (Yes)
* Modification: Can modify input array? (Yes)

**3. Hand Trace**
Input: `[[1, 3], [1, 2], [2, 4], [3, 5]]`

* Order chronologically by start: `[1, 2], [1, 3], [2, 4], [3, 5]`
* Compare `[1,2]` and `[1,3]`. Overlap. Which to drop? Drop `[1,3]` because it ends later, blocking more future space.
* Kept end: `2`. Removals: `1`.


* Next: `[2,4]`. Starts at `2`. Kept end `2`. No overlap.
* Kept end: `4`. Removals: `1`.


* Next: `[3,5]`. Starts at `3`. Kept end `4`. Overlap. Drop `[3,5]` (ends later).
* Kept end: `4`. Removals: `2`.
Output: `2`.



**4. Brainstorming & Complexity**

* *Backtracking*: Try removing/keeping each interval. $O(2^n)$ time. Too slow.
* *Dynamic Programming*: Sort by start, find max valid subsequence. $O(n^2)$ time.
* *Greedy*: Process left-to-right. Sort by start. When overlapping, greedily drop the one ending later. $O(n \log n)$ time for sorting. $O(1)$ space. Maps exactly to hand trace.

**5. Suggestions**

1. Dynamic Programming (Longest non-overlapping subsequence).
2. Greedy approach (Sort by start, track end times, drop later ends).
*Selection*: Greedy. Simple, straight forward, mirrors human logic.

**6. Outline**

```python
def eraseOverlapIntervals(intervals):
    """
    Reframe: Min removals = max non-overlapping. Greedily keep intervals ending earliest.
    State: `last_kept_end`, chosen because only the rightmost bound determines future overlaps.
    Invariant: `last_kept_end` tracks the earliest possible end time of the valid chain.

    sort_by_start(intervals) = sorts list chronologically
    overlaps(curr, last_end) = true if current interval starts before last_end
    ends_earlier(curr, last_end) = true if current interval ends before last_end

    Core logic:
    - sort intervals by start time
    - initialize removal counter to zero
    - set last_kept_end to first interval's end
    - for each subsequent interval:
        - if it overlaps with last_kept_end:
            - increment removal counter
            - if it ends_earlier than last_kept_end:
                - update last_kept_end to current interval's end
        - else (no overlap):
            - update last_kept_end to current interval's end

    Edge cases:
    - empty intervals list -> return 0
    - list of size 1 -> return 0
    """

```

**7. Iterative Implementation**

*Iteration 1: Skeleton with helpers*

```python
def eraseOverlapIntervals(intervals):
    intervals = sort_by_start(intervals)
    removals = 0
    
    # TODO: initialize state
    # TODO: loop through intervals
    
    return removals

```

*Iteration 2: Core logic flow (plain English to code structure)*

```python
def eraseOverlapIntervals(intervals):
    intervals = sort_by_start(intervals)
    removals = 0
    
    last_kept_end = get_end(intervals[0])
    
    for curr in get_subsequent(intervals):
        if overlaps(curr, last_kept_end):
            removals += 1
            if ends_earlier(curr, last_kept_end):
                last_kept_end = get_end(curr)
        else:
            last_kept_end = get_end(curr)
            
    return removals

```

*Iteration 3: Replace helpers with array logic (realizing core logic)*

```python
def eraseOverlapIntervals(intervals):
    # sort by start time
    intervals.sort(key=lambda x: x[0])
    removals = 0
    
    last_kept_end = intervals[0][1]
    
    # loop from second element onward
    for i in range(1, len(intervals)):
        curr_start = intervals[i][0]
        curr_end = intervals[i][1]
        
        if curr_start < last_kept_end: # overlaps
            removals += 1
            if curr_end < last_kept_end: # ends_earlier
                last_kept_end = curr_end
        else: # no overlap
            last_kept_end = curr_end
            
    return removals

```

*Iteration 4: Patching Edge Cases (Empty array breaks `intervals[0]`)*

```python
def eraseOverlapIntervals(intervals):
    # EDGE CASE: empty or single interval
    if not intervals or len(intervals) <= 1:
        return 0

    intervals.sort(key=lambda x: x[0])
    removals = 0
    
    last_kept_end = intervals[0][1]
    
    for i in range(1, len(intervals)):
        curr_start = intervals[i][0]
        curr_end = intervals[i][1]
        
        if curr_start < last_kept_end:
            removals += 1
            if curr_end < last_kept_end:
                last_kept_end = curr_end
        else:
            last_kept_end = curr_end
            
    return removals

```

**8. Complexity & Optimization**

* *Time Complexity*: $O(n \log n)$ due to Python's Timsort. The iterative sweep is $O(n)$.
* *Space Complexity*: $O(n)$ or $O(1)$ depending on sort implementation under the hood.

*Optimization*: Sorting by **start time** forces us to check which overlapping interval ends earlier.
If we sort by **end time** upfront, we *guarantee* we are always processing the interval that ends earliest first. The logic collapses. We never have to compare end times during an overlap—we just blindly drop overlapping intervals.

*Optimized Code Outline:*

```python
def eraseOverlapIntervals_optimized(intervals):
    if not intervals: return 0
    
    # Sort by END time
    intervals.sort(key=lambda x: x[1])
    
    last_kept_end = intervals[0][1]
    removals = 0
    
    for i in range(1, len(intervals)):
        if intervals[i][0] < last_kept_end:
            # Overlaps. We know curr ends later (or equal) due to sort. Just drop it.
            removals += 1
        else:
            # No overlap. Update end.
            last_kept_end = intervals[i][1]
            
    return removals

```