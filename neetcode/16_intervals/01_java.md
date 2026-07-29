### 1. Restate the problem

We are given a list of non-overlapping intervals that are already sorted by their start times. We are also given a single new interval. Our goal is to insert this new interval into the correct position so that the list remains sorted. If the new interval overlaps with any existing intervals, we must merge them together into a single, continuous interval. Finally, we need to return the updated list of non-overlapping intervals.

### 2. Ask clarifying questions

Before writing code, I'd like to confirm a few details about the inputs and constraints:

* **Input size:** How large can the `intervals` array be? (Assumption: It can be empty, or up to roughly $10^4$ elements.)
* **Boundaries:** Are the interval boundaries inclusive? (Assumption: Yes, as stated in the prompt, `[1,2]` and `[2,3]` overlap at `2`.)
* **Data Types:** Since Java arrays have a fixed size, I assume I should return a newly allocated `int[][]` rather than trying to modify the input array in place? (Assumption: Yes, return a new 2D array.)
* **Negative values:** Can start and end times be negative? (Assumption: Yes, but it shouldn't change the comparison logic.)

### 3. Work through an example by hand

Let's trace a slightly complex example to see the merging behavior clearly.

* `intervals = [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]]`
* `newInterval = [4, 8]`

**Step-by-step trace:**

1. **Look at `[1, 2]`:** The end time `2` is less than the new start time `4`. It's completely before the new interval.
* *Result so far:* `[[1, 2]]`


2. **Look at `[3, 5]`:** The end time `5` is $\ge$ `4`, and the start time `3` is $\le$ `8`. They overlap! We merge them into a single interval covering the minimum start and maximum end: `[min(3, 4), max(5, 8)]` = `[3, 8]`. The `newInterval` is now functionally `[3, 8]`.
* *Result so far:* `[[1, 2]]` (waiting to finalize `[3, 8]`)


3. **Look at `[6, 7]`:** The start time `6` is $\le$ `8`. It overlaps with our updated `newInterval`. Merge them: `[min(3, 6), max(8, 7)]` = `[3, 8]`.
4. **Look at `[8, 10]`:** The start time `8` is $\le$ `8`. It overlaps! Merge: `[min(3, 8), max(8, 10)]` = `[3, 10]`.
5. **Look at `[12, 16]`:** The start time `12` is $>$ `10`. It is strictly after our merged interval. This means our merged interval `[3, 10]` is finalized.
* *Result so far:* `[[1, 2], [3, 10]]`


6. **Remaining intervals:** Add `[12, 16]` directly.
* *Final Result:* `[[1, 2], [3, 10], [12, 16]]`



### 4. Brainstorm solutions aloud

* **Approach 1: Append, Sort, and Merge**
* *Idea:* Add `newInterval` to the end of `intervals`. Re-sort the whole list by start times. Then iterate through and merge adjacent overlapping intervals.
* *Complexity:* $O(N \log N)$ time due to sorting, $O(N)$ space.
* *Tradeoffs:* Very simple to write if you already have a standard merge-intervals function, but it entirely ignores the fact that the input is *already* sorted, doing unnecessary work.


* **Approach 2: Linear Scan (Three Phases)**
* *Idea:* As seen in the manual example, the intervals naturally fall into three groups: those strictly before `newInterval`, those that overlap with it, and those strictly after. We can iterate through the array once and handle each phase sequentially.
* *Complexity:* $O(N)$ time since we look at each interval exactly once. $O(N)$ space to store the results.
* *Tradeoffs:* Optimal time complexity and leverages the existing sorted order.


* **Approach 3: Binary Search**
* *Idea:* Use binary search to find the insertion index of `newInterval`'s start and end times to identify the exact sub-array of overlaps.
* *Complexity:* $O(\log N)$ to find the indices, but still $O(N)$ to shift elements or copy the non-overlapping parts into a new array.
* *Tradeoffs:* Does not improve the overall $O(N)$ theoretical bound and introduces significant boundary-condition complexity.



### 5. Select the solution

I will go with **Approach 2: Linear Scan (Three Phases)**. It is optimal ($O(N)$ time), easy to explain, and naturally translates the logic we verified by hand into code. We'll use a `List<int[]>` (specifically an `ArrayList`) to build the sequence because we don't know the exact size of the final array until we're done merging.

### 6. Write the implementation outline

```java
int[][] insert(int[][] intervals, int[] newInterval) {
    /*
     * Reframe:
     * Partition the existing intervals into three contiguous groups:
     * entirely before the new interval, overlapping, and entirely after.
     *
     * State:
     * An ArrayList to dynamically accumulate the final intervals.
     * Chosen because the final size is unknown due to potential merges.
     *
     * Invariant:
     * The list of results remains strictly sorted and non-overlapping at all times.
     *
     * Core logic:
     * - Phase 1: iterate and add all intervals that end before newInterval starts.
     * - Phase 2: iterate and merge all intervals that overlap with newInterval.
     *   Update newInterval's start and end to the bounding min and max.
     * - Add the fully merged newInterval to the results.
     * - Phase 3: iterate and add all remaining intervals.
     * - Convert the dynamic list back to a 2D array.
     *
     * Edge cases:
     * - Empty input array.
     * - newInterval is placed entirely at the beginning.
     * - newInterval is placed entirely at the end.
     * - newInterval engulfs all existing intervals.
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton and control flow**
Set up the list, the loop variables, and structural TODOs.

```java
public int[][] insert(int[][] intervals, int[] newInterval) {
    List<int[]> result = new ArrayList<>();
    int i = 0;
    int n = intervals.length;

    // TODO: Phase 1 - Add all intervals ending before newInterval starts

    // TODO: Phase 2 - Merge all overlapping intervals

    // TODO: Phase 3 - Add the remaining intervals

    // Convert ArrayList back to int[][]
    return result.toArray(new int[result.size()][]);
}

```

**Iteration 2: Implement Phase 1 and Phase 3 (the easy parts)**
Write the loops for the intervals that are completely untouched by the new interval.

```java
public int[][] insert(int[][] intervals, int[] newInterval) {
    List<int[]> result = new ArrayList<>();
    int i = 0;
    int n = intervals.length;

    // Added: Phase 1. An interval is completely before if its end time
    // is strictly less than the new interval's start time.
    while (i < n && intervals[i][1] < newInterval[0]) {
        result.add(intervals[i]);
        i++;
    }

    // TODO: Phase 2 - Merge all overlapping intervals
    
    // Added: Phase 3. Add all remaining intervals after the merge is done.
    while (i < n) {
        result.add(intervals[i]);
        i++;
    }

    return result.toArray(new int[result.size()][]);
}

```

**Iteration 3: Complete the core logic (Phase 2)**
Now, let's implement the overlapping logic. An interval overlaps if its start time is $\le$ the new interval's end time.

```java
public int[][] insert(int[][] intervals, int[] newInterval) {
    List<int[]> result = new ArrayList<>();
    int i = 0;
    int n = intervals.length;

    // Phase 1: intervals strictly before newInterval
    while (i < n && intervals[i][1] < newInterval[0]) {
        result.add(intervals[i]);
        i++;
    }

    // Added: Phase 2. While the current interval starts before or at the 
    // exact moment the newInterval ends, they overlap.
    while (i < n && intervals[i][0] <= newInterval[1]) {
        // Expand newInterval to encompass the merged bounds
        newInterval[0] = Math.min(newInterval[0], intervals[i][0]);
        newInterval[1] = Math.max(newInterval[1], intervals[i][1]);
        i++;
    }
    // The merged interval is finalized, add it to the result
    result.add(newInterval);

    // Phase 3: intervals strictly after newInterval
    while (i < n) {
        result.add(intervals[i]);
        i++;
    }

    return result.toArray(new int[result.size()][]);
}

```

**Edge-case pass**
Let's review the edge cases identified earlier:

* *Empty input:* If `intervals` is `[]`, `n = 0`. The first loop skips, the second skips, `newInterval` is added, the third skips. Returns `[newInterval]`. Correct.
* *Placed entirely at beginning:* `newInterval` ends before the first interval starts. Phase 1 skips, Phase 2 skips, `newInterval` added first, Phase 3 adds the rest. Correct.
* *Placed entirely at end:* Phase 1 adds everything, Phase 2 skips, `newInterval` added at the end, Phase 3 skips. Correct.
* *Engulfs all intervals:* Phase 1 skips, Phase 2 merges everything into `newInterval`, `newInterval` is added, Phase 3 skips. Correct.

No additional defensive checks or patches are needed. The three-phase logic naturally protects against these edge cases.

### 8. Analyze expensive sections and optimize (Final Code)

The implementation looks solid.

* **Time Complexity:** $O(N)$. We iterate through the `intervals` array exactly once. The `Math.min` and `Math.max` operations take $O(1)$ time. Converting the `ArrayList` to a 2D array takes another $O(N)$ pass. Total time is strictly $O(N)$.
* **Space Complexity:** $O(N)$ to store the `result` list. If the interviewer doesn't count the returned array towards space complexity, then auxiliary space is $O(1)$ except for the intermediate list resizing.

Here is the clean, final version of the code:

```java
import java.util.ArrayList;
import java.util.List;

class Solution {
    public int[][] insert(int[][] intervals, int[] newInterval) {
        List<int[]> result = new ArrayList<>();
        int i = 0;
        int n = intervals.length;

        // Phase 1: Add all intervals that end before the new interval starts
        while (i < n && intervals[i][1] < newInterval[0]) {
            result.add(intervals[i]);
            i++;
        }

        // Phase 2: Merge all intervals that overlap with the new interval
        // An interval overlaps if its start time is <= the new interval's end time
        while (i < n && intervals[i][0] <= newInterval[1]) {
            newInterval[0] = Math.min(newInterval[0], intervals[i][0]);
            newInterval[1] = Math.max(newInterval[1], intervals[i][1]);
            i++;
        }
        result.add(newInterval);

        // Phase 3: Add all remaining intervals that start after the new interval ends
        while (i < n) {
            result.add(intervals[i]);
            i++;
        }

        // Convert the dynamic list to a 2D array
        return result.toArray(new int[result.size()][]);
    }
}

```

### 9. Brief test walkthrough

Let's test this with a case where the new interval engulfs the center elements:

* `intervals = [[1,2], [3,5], [6,7], [8,10], [12,16]]`
* `newInterval = [4,8]`

1. **Phase 1:** `i = 0`, interval `[1,2]`. End `2` < `4`. Add `[1,2]`. `i = 1`.
`i = 1`, interval `[3,5]`. End `5` is NOT < `4`. Phase 1 ends.
2. **Phase 2:** `i = 1`, interval `[3,5]`. Start `3` $\le$ `8`. Overlaps. `newInterval` becomes `[min(4,3), max(8,5)]` = `[3,8]`. `i = 2`.
`i = 2`, interval `[6,7]`. Start `6` $\le$ `8`. Overlaps. `newInterval` becomes `[min(3,6), max(8,7)]` = `[3,8]`. `i = 3`.
`i = 3`, interval `[8,10]`. Start `8` $\le$ `8`. Overlaps. `newInterval` becomes `[min(3,8), max(8,10)]` = `[3,10]`. `i = 4`.
`i = 4`, interval `[12,16]`. Start `12` is NOT $\le$ `10`. Phase 2 ends.
Result list gets `[3,10]`.
3. **Phase 3:** `i = 4`, interval `[12,16]`. Add `[12,16]`. Loop ends.
4. **Final Array:** `[[1,2], [3,10], [12,16]]`. Matches the manual example perfectly.