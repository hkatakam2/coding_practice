### question
You are given an array of non-overlapping intervals intervals where intervals[i] = [start_i, end_i] represents the start and the end time of the ith interval. intervals is initially sorted in ascending order by start_i.

You are given another interval newInterval = [start, end].

Insert newInterval into intervals such that intervals is still sorted in ascending order by start_i and also intervals still does not have any overlapping intervals. You may merge the overlapping intervals if needed.

Return intervals after adding newInterval.

Note: Intervals are non-overlapping if they have no common point. For example, [1,2] and [3,4] are non-overlapping, but [1,2] and [2,3] are overlapping.


**1. Restate**
Given sorted list of non-overlapping intervals and one new interval. Insert new interval into list, merge if overlaps occur. Return updated sorted list of disjoint intervals.

**2. Clarify**

* Input: `intervals` (List of `[start, end]`), `newInterval` (`[start, end]`).
* Output: List of `[start, end]`.
* Q: Intervals inclusive? A: Yes. `[1,2]` and `[2,3]` overlap.
* Q: Empty list possible? A: Yes.
* Q: Already sorted by start time? A: Yes.

**3. Example by Hand**
`intervals = [[1,2], [3,5], [6,7], [8,10], [12,16]]`, `newInterval = [4,8]`

* `[1,2]`: ends at 2. 2 < 4. Strictly before. Keep: `[[1,2]]`
* `[3,5]`: overlaps `[4,8]`. Merge -> `[3,8]` (update newInterval, don't add yet)
* `[6,7]`: overlaps `[3,8]`. Merge -> `[3,8]`
* `[8,10]`: overlaps `[3,8]`. Merge -> `[3,10]`
* `[12,16]`: starts at 12. 12 > 10. Strictly after. First add merged `[3,10]`, then `[12,16]`.
* Result: `[[1,2], [3,10], [12,16]]`

**4. Brainstorm**

* *Approach A:* Append `newInterval`, sort by start, run standard interval merge. Time: $O(N \log N)$. Space: $O(N)$.
* *Approach B:* Binary Search insertion point. Find start/end bounds. Slicing. Time: $O(N)$ because array shifting/copying still takes $O(N)$, though search is $O(\log N)$. Space: $O(N)$.
* *Approach C:* Linear Scan. Mimics hand-example. 3 phases: before, overlapping, after. Time: $O(N)$. Space: $O(N)$.

**5. Suggest**
Prefer Approach C (Linear Scan). Simple, clear, directly maps to human logic. No complex binary search index tracking. No unnecessary sorting.

**6. Outline**

```python
def insert(intervals, newInterval):
    """
    Reframe: Divide intervals into three distinct buckets relative to newInterval: strictly before, overlapping, strictly after.
    State: Result list maintained, chosen because we build the new disjoint set incrementally left-to-right.
    Invariant: Result list always contains sorted, disjoint intervals up to current scan point.

    is_before(curr, new) = true if curr ends before new starts.
    is_after(curr, new) = true if curr starts after new ends.
    merge(curr, new) = returns single bounding interval covering both.

    Core logic:
    - loop over all intervals
    - if current is before new: append current to result
    - if current is after new: 
        append new to result (if not done yet)
        append current to result
    - if current overlaps new:
        merge current and new into a combined new interval (do not append yet)
    - after loop, append new to result if never added

    Edge cases:
    - intervals is empty list
    - newInterval belongs at very end (never hits "after" condition)
    - newInterval belongs at very beginning (never hits "before" condition)
    """

```

**7. Iterative Implementation**

*Iteration 1: Skeleton with stubs*

```python
def insert(intervals, newInterval):
    res = []
    new_added = False
    
    # stubs
    def is_before(curr, new): return False
    def is_after(curr, new): return False
    def merge(curr, new): return []
    
    for interval in intervals:
        if is_before(interval, newInterval):
            # TODO: add current
            pass
        elif is_after(interval, newInterval):
            # TODO: add new if needed, add current
            pass
        else:
            # TODO: merge
            pass
            
    # TODO: add new if never added
    return res

```

*Iteration 2: Fill helpers and core loop*

```python
def insert(intervals, newInterval):
    res = []
    new_added = False
    
    # helper implementations
    def is_before(curr, new): return curr[1] < new[0]
    def is_after(curr, new): return curr[0] > new[1]
    def merge(curr, new): return [min(curr[0], new[0]), max(curr[1], new[1])]
    
    for interval in intervals:
        if is_before(interval, newInterval):
            res.append(interval) # added current
            
        elif is_after(interval, newInterval):
            if not new_added:
                res.append(newInterval) # added new
                new_added = True
            res.append(interval) # added current
            
        else:
            newInterval = merge(interval, newInterval) # merged state updated
            
    if not new_added:
        res.append(newInterval)
        
    return res

```

*Iteration 3: Inline helpers for standard Python style, patch edge cases*
*Checking Edge Cases from step 6:*

* Empty `intervals`: loop skipped, `new_added` is False, appends `newInterval`, returns `[[start, end]]`. (Works).
* Goes at very end: loop processes all as `is_before`, `new_added` stays False. Appends at end. (Works).
* Goes at very beginning: loop hits `is_after` immediately. Appends `newInterval`, flags `new_added`, appends rest. (Works).

*Final Code (inlining helpers for brevity):*

```python
def insert(intervals, newInterval):
    res = []
    new_added = False
    
    for interval in intervals:
        # is_before
        if interval[1] < newInterval[0]:
            res.append(interval)
            
        # is_after
        elif interval[0] > newInterval[1]:
            if not new_added:
                res.append(newInterval)
                new_added = True
            res.append(interval)
            
        # overlapping
        else:
            newInterval = [
                min(interval[0], newInterval[0]), 
                max(interval[1], newInterval[1])
            ]
            
    if not new_added:
        res.append(newInterval)
        
    return res

```

**8. Complexity & Optimizations**

* **Time Complexity:** $O(N)$ where $N$ is length of intervals. We visit each interval exactly once.
* **Space Complexity:** $O(N)$ to build `res` array.
* **Optimization:** In current code, once we hit `is_after`, we keep checking `if not new_added` on every subsequent interval. We can avoid this and early exit the loop by just slicing the rest of the array.

*Optimized Code snippet:*

```python
def insert(intervals, newInterval):
    res = []
    
    for i, interval in enumerate(intervals):
        if interval[1] < newInterval[0]:
            res.append(interval)
        elif interval[0] > newInterval[1]:
            # Found strictly after. Add newInterval, then dump remaining list.
            res.append(newInterval)
            return res + intervals[i:] # optimization: bulk append
        else:
            # Overlap
            newInterval = [min(interval[0], newInterval[0]), max(interval[1], newInterval[1])]
            
    # If we finish loop without hitting 'after' condition
    res.append(newInterval)
    return res

```

*Note:* The optimization removes the need for `new_added` state entirely, simplifying the code further. Time remains $O(N)$, but practical runtime is faster due to array slicing.