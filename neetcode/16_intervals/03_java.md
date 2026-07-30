### 1. Restate the problem

We are given a list of intervals, each defined by a start and end time. We need to find the minimum number of intervals to delete so that all remaining intervals do not overlap.

Intervals are considered non-overlapping if they only touch at their boundaries (e.g., an interval ending at 3 and another starting at 3 do not overlap).

### 2. Ask clarifying questions

Before writing code, I would confirm a few details:

* **Input size:** How many intervals can we expect? (Assume up to $10^5$, meaning an $O(n^2)$ solution will be too slow).
* **Input mutation:** Can I sort the input array in place? (Assume yes. If not, I would clone it first).
* **Negative values:** Can intervals have negative start/end times? (Assume yes).
* **Bounds:** Can `start` and `end` values exceed normal integer limits, causing overflow if subtracted? (Assume standard 32-bit signed integers, so I should avoid subtraction in comparators to prevent overflow).
* **Empty input:** Can the input array be empty? (Assume the length can be 0, though I will handle it gracefully).

### 3. Work through an example by hand

Let's trace the input: `[[1, 2], [2, 3], [3, 4], [1, 3]]`

If we visualize them on a timeline:

* A: `[1, 2]`
* B: `[2, 3]`
* C: `[3, 4]`
* D: `[1, 3]`

If I keep `D [1, 3]`, it overlaps with `A [1, 2]` and `B [2, 3]`. I would have to remove both A and B, leaving me with `D [1, 3]` and `C [3, 4]`. That requires **2 removals**.
If I keep `A [1, 2]`, it doesn't overlap with `B [2, 3]`. `B` doesn't overlap with `C [3, 4]`. But `D [1, 3]` overlaps with A and B. I can just remove `D`. That requires **1 removal**.

The minimum removals is 1. We want to consistently prioritize intervals that "finish early", as they leave the maximum possible room for subsequent intervals.

### 4. Brainstorm solutions aloud

**Approach 1: Brute Force (Subsets)**

* *Core idea:* Generate every possible combination of intervals. Check which combinations have no overlaps, and find the largest such valid set.
* *Complexity:* $O(2^n)$ time, which is completely unscalable.

**Approach 2: Greedy with Start-Time Sorting**

* *Core idea:* Sort all intervals by their start times. Iterate through them. If two intervals overlap, we are forced to drop one. To minimize future overlaps, we should drop the one that ends *later*.
* *Complexity:* $O(n \log n)$ time for sorting, $O(1)$ space.

**Approach 3: Greedy with End-Time Sorting (Interval Scheduling Maximization)**

* *Core idea:* Sort all intervals by their *end* times. We greedily pick the interval that ends the earliest because it consumes the least amount of the remaining timeline. If the next interval starts before the current one finishes, we must drop it.
* *Complexity:* $O(n \log n)$ time for sorting, $O(n)$ time for one sweep. Total time $O(n \log n)$.
* *Why it works:* Every time we pick the earliest ending interval, we leave the maximum possible room for the rest. This mathematically guarantees the maximum number of non-overlapping intervals (and thus the minimum removals).

### 5. Select the solution

I will go with **Approach 3 (Greedy with End-Time Sorting)**.
It is standard, extremely readable, and guarantees optimal time complexity ($O(n \log n)$). It allows us to process the array in a single sweep after sorting, without needing to look backward or maintain complex data structures. I will use `Arrays.sort` with a custom `Comparator` via `Comparator.comparingInt` to avoid overflow bugs.

### 6. Write the implementation outline

```java
int eraseOverlapIntervals(int[][] intervals) {
    /*
     * Reframe:
     * Find the maximum number of intervals we can keep by always picking the 
     * one that ends earliest. Count the ones we are forced to skip.
     *
     * State:
     * - removedCount: tally of intervals we drop.
     * - lastValidEnd: the end time of the last kept interval.
     * Chosen because tracking the end of our current valid chain tells us 
     * exactly when the next interval can safely start.
     *
     * Invariant:
     * 'lastValidEnd' always tracks the smallest possible end time among all 
     * validly selected, non-overlapping intervals so far.
     *
     * Core logic:
     * - handle empty arrays early.
     * - sort the intervals ascending by their end time.
     * - initialize lastValidEnd to the end time of the very first interval.
     * - loop through the remaining intervals:
     *     - if the current interval starts before lastValidEnd, it overlaps. 
     *       Increment removedCount.
     *     - otherwise, it doesn't overlap. Update lastValidEnd to this 
     *       interval's end time.
     *
     * Edge cases:
     * - completely identical intervals (e.g., [1,2] and [1,2])
     * - one interval completely swallowing another (handled naturally by sorting)
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton**
I will set up the method signature, validation, and the structural skeleton.

```java
public int eraseOverlapIntervals(int[][] intervals) {
    if (intervals == null || intervals.length <= 1) {
        return 0; // Nothing to remove if 1 or 0 intervals
    }

    int removedCount = 0;

    // TODO: Sort intervals by end time
    // TODO: Iterate through and count overlaps
    
    return removedCount;
}

```

**Iteration 2: Sorting and state setup**
Next, I apply the sorting logic using standard Java 17 features.

```java
public int eraseOverlapIntervals(int[][] intervals) {
    if (intervals == null || intervals.length <= 1) {
        return 0;
    }

    // Added: Sort by end time. 
    // Using comparingInt avoids integer overflow that a->a[1]-b[1] might cause.
    Arrays.sort(intervals, Comparator.comparingInt(interval -> interval[1]));

    int removedCount = 0;
    // Added: Initialize our tracking variable with the first interval's end.
    int lastValidEnd = intervals[0][1];

    // TODO: Iterate through the remaining intervals and count overlaps
    
    return removedCount;
}

```

**Iteration 3: Complete the happy path**
Finally, I will iterate starting from the second element, applying the greedy choice logic.

```java
public int eraseOverlapIntervals(int[][] intervals) {
    if (intervals == null || intervals.length <= 1) {
        return 0;
    }

    Arrays.sort(intervals, Comparator.comparingInt(interval -> interval[1]));

    int removedCount = 0;
    int lastValidEnd = intervals[0][1];

    // Added: Sweep through intervals starting from index 1.
    for (int i = 1; i < intervals.length; i++) {
        int currentStart = intervals[i][0];
        int currentEnd = intervals[i][1];

        if (currentStart < lastValidEnd) {
            // Overlap detected. Since we sorted by end time, the current 
            // interval ends later than (or equal to) lastValidEnd. We remove it.
            removedCount++;
        } else {
            // No overlap. We keep this interval and advance our tracking end time.
            lastValidEnd = currentEnd;
        }
    }

    return removedCount;
}

```

### 8. Edge-case pass and final optimizations

Let's review the edge cases:

* **Empty or size 1 input:** Handled safely by the initial `intervals.length <= 1` check.
* **Identical intervals (e.g. `[[1,2], [1,2]]`):** Sort order doesn't matter. The first becomes `lastValidEnd = 2`. The second starts at `1 < 2`, so it counts as removed. Correct.
* **Fully enclosed intervals (e.g. `[[1,4], [2,3]]`):** Sorting by end time puts `[2,3]` first. `lastValidEnd = 3`. Next is `[1,4]`, its start `1 < 3`, so it gets dropped. This correctly drops the wider interval that eats up more timeline.

There are no expensive sections inside the loop. `Arrays.sort` is the bottleneck, which is unavoidable for this greedy strategy. No further optimizations are needed.

### Final Code

```java
public int eraseOverlapIntervals(int[][] intervals) {
    if (intervals == null || intervals.length <= 1) {
        return 0;
    }

    // Sort intervals by their end time.
    // Comparator.comparingInt is immune to integer overflow bugs.
    Arrays.sort(intervals, Comparator.comparingInt(interval -> interval[1]));

    int removedCount = 0;
    int lastValidEnd = intervals[0][1];

    for (int i = 1; i < intervals.length; i++) {
        int currentStart = intervals[i][0];
        int currentEnd = intervals[i][1];

        if (currentStart < lastValidEnd) {
            // It starts before the previous interval finishes. We must drop it.
            removedCount++;
        } else {
            // It fits. Keep it and update the end time marker.
            lastValidEnd = currentEnd;
        }
    }

    return removedCount;
}

```

### Complexity

* **Time Complexity:** `O(n log n)`. The sorting operation dominates the time complexity. The subsequent linear sweep takes `O(n)` time.
* **Space Complexity:** `O(log n)` to `O(n)`. We don't allocate any extra data structures, but Java's `Arrays.sort()` (which uses Dual-Pivot Quicksort for primitives, and TimSort for Objects) requires `O(log n)` memory for its call stack.

### Brief test walkthrough

Let's run `[[1, 2], [2, 3], [3, 4], [1, 3]]` through the final code.

1. `Arrays.sort` by end times:
`[1, 2]` (ends 2), `[2, 3]` (ends 3), `[1, 3]` (ends 3), `[3, 4]` (ends 4).
*Sorted:* `[[1, 2], [2, 3], [1, 3], [3, 4]]`
2. `removedCount = 0`, `lastValidEnd = 2`.
3. `i = 1`: `[2, 3]`. `currentStart (2) < lastValidEnd (2)` is false.
No overlap. `lastValidEnd = 3`.
4. `i = 2`: `[1, 3]`. `currentStart (1) < lastValidEnd (3)` is true.
Overlap! `removedCount = 1`.
5. `i = 3`: `[3, 4]`. `currentStart (3) < lastValidEnd (3)` is false.
No overlap. `lastValidEnd = 4`.
6. Loop finishes. Returns `1`. The correct answer.