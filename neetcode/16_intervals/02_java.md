### 1. Restate the problem

We are given a collection of intervals, where each interval has a start and an end. Our task is to combine any intervals that overlap into a single, continuous interval. The final result should be a list of disjoint (non-overlapping) intervals that covers the exact same ranges as the original input.

### 2. Ask clarifying questions and state assumptions

In a real interview, I would confirm the following:

* **Can the input array be empty?**
*Assumption:* Yes. I should handle an empty input gracefully.
* **Is the input sorted?**
*Assumption:* No. The intervals could be in any order.
* **Are the start times always less than or equal to the end times?**
*Assumption:* Yes, `start_i <= end_i`.
* **Can I modify the input array?**
*Assumption:* Sorting the input array in place is acceptable. If the caller requires the original array to remain untouched, I would make a copy first. For this solution, I will sort the input directly to save memory.
* **How do we handle adjacent intervals like `[1, 2]` and `[2, 3]`?**
*Assumption:* The problem description states they are considered overlapping, so they should be merged into `[1, 3]`.

### 3. Work through an example by hand

Let's take a representative, unsorted input: `[[2, 6], [1, 3], [15, 18], [8, 10], [1, 4]]`.

1. **Sort the intervals by their start times:**
`[[1, 3], [1, 4], [2, 6], [8, 10], [15, 18]]`
2. **Initialize:**
Take the first interval `[1, 3]` and hold it as our `current` interval.
3. **Compare with the next `[1, 4]`:**
The start of `[1, 4]` is `1`, which is `<= 3` (the end of `current`). They overlap.
Merge them: the new end is `max(3, 4) = 4`. `current` becomes `[1, 4]`.
4. **Compare with the next `[2, 6]`:**
The start of `[2, 6]` is `2`, which is `<= 4`. They overlap.
Merge them: the new end is `max(4, 6) = 6`. `current` becomes `[1, 6]`.
5. **Compare with the next `[8, 10]`:**
The start of `[8, 10]` is `8`, which is `> 6`. No overlap.
Push `current` `[1, 6]` to our final result list.
Set `current` to `[8, 10]`.
6. **Compare with the next `[15, 18]`:**
The start of `[15, 18]` is `15`, which is `> 10`. No overlap.
Push `current` `[8, 10]` to our final result list.
Set `current` to `[15, 18]`.
7. **End of list:**
Push the last `current` `[15, 18]` to the result list.

Final Result: `[[1, 6], [8, 10], [15, 18]]`.

### 4. Candidate solutions

* **Direct Simulation / Connected Components (Brute Force):** Compare every interval with every other interval to see if they overlap. If they do, merge them, replace them in the list, and repeat until no more merges can happen.
*Time:* $O(n^2)$ or even $O(n^3)$ depending on implementation.
*Space:* $O(n)$.
*Tradeoffs:* Too slow for large inputs, difficult to implement cleanly without bugs.
* **Sorting and Sweeping (Two Pointers / Accumulator):** Sort the intervals by their starting times. By doing this, any overlapping intervals will be adjacent in the sorted array. We can then sweep through the array once, keeping track of the current active interval and expanding its end time whenever we encounter an overlap.
*Time:* $O(n \log n)$ due to sorting. The sweep is $O(n)$.
*Space:* $O(\log n)$ to $O(n)$ for the sorting algorithm's auxiliary space, plus space for the output.
*Tradeoffs:* Very efficient, clean to read, relies on standard library sorting.

### 5. Selected solution and justification

I will proceed with the **Sorting and Sweeping** approach. It is the optimal way to solve this problem because sorting reduces a complex $O(n^2)$ pair-matching problem into a simple $O(n)$ linear scan. I'll use a `List<int[]>` to collect the merged intervals dynamically, then convert it back to an `int[][]` array at the end.

### 6. Plain-English implementation outline

```java
int[][] merge(int[][] intervals) {
    /*
     * Reframe:
     * Sort intervals by start time so overlaps are adjacent, then merge them in a single pass.
     *
     * State:
     * A dynamically sized List to store merged intervals.
     * A reference to the 'current' interval being expanded.
     * Chosen because we don't know the final size of the output array in advance.
     *
     * Invariant:
     * The 'current' interval always contains the earliest start time of the current
     * overlapping cluster, and its end time is the maximum end time seen so far in this cluster.
     *
     * Core logic:
     * - sort the input array based on the first element of each interval
     * - store the first interval as the 'current' interval and add it to our result list
     * - inspect each subsequent interval
     * - if the subsequent interval starts before or when the 'current' interval ends, they overlap
     * - update the 'current' interval's end time to the maximum of both end times
     * - if they do not overlap, the subsequent interval becomes the new 'current' interval
     *   and is added to the result list
     * - return the result list converted to an array
     *
     * Edge cases:
     * - empty input array
     * - fully swallowed intervals (e.g., [1, 10] and [2, 3])
     */
}

```

### 7. Iterative Java implementation

#### Iteration 1: Method skeleton

First, I will set up the sorting, the state variables, and the return conversion.

```java
public int[][] merge(int[][] intervals) {
    // Edge case: handle empty arrays immediately
    if (intervals == null || intervals.length == 0) {
        return new int[0][];
    }

    // Sort by start time using standard library tools
    Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));

    List<int[]> merged = new ArrayList<>();
    
    // TODO: initialize the current interval and add it to merged list
    // TODO: loop through remaining intervals to merge or append
    
    return merged.toArray(new int[0][]);
}

```

#### Iteration 2: Implement the core loop (Happy Path)

Now I will add the linear scan, checking for overlaps based on our established invariant. Notice I will add the `currentInterval` by reference to the `merged` list. This means when I mutate `currentInterval[1]` (the end time), the change is automatically reflected in the `merged` list!

```java
public int[][] merge(int[][] intervals) {
    if (intervals == null || intervals.length == 0) {
        return new int[0][];
    }

    Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));

    List<int[]> merged = new ArrayList<>();
    
    // Added: Initialize the first interval
    int[] currentInterval = intervals[0];
    merged.add(currentInterval);
    
    for (int i = 1; i < intervals.length; i++) {
        int[] nextInterval = intervals[i];
        
        // Added: Check for overlap. 
        // Because the list is sorted, we only need to compare next's start with current's end.
        if (nextInterval[0] <= currentInterval[1]) {
            // Overlap exists: mutate the current interval in place
            currentInterval[1] = Math.max(currentInterval[1], nextInterval[1]);
        } else {
            // No overlap: transition state to the new interval
            currentInterval = nextInterval;
            merged.add(currentInterval);
        }
    }
    
    return merged.toArray(new int[0][]);
}

```

#### Edge-case pass

Let's review the edge cases identified earlier against our current logic.

* **Empty Input:** Handled safely by the initial `if` check.
* **One Element:** The loop starts at `i = 1`, bypassing the loop entirely, and returns the single element correctly.
* **Fully swallowed interval (`[[1, 10], [2, 3]]`):** Sorted order is `[[1, 10], [2, 3]]`. `nextInterval[0]` is `2`, which is `<= 10`. `currentInterval[1]` becomes `Math.max(10, 3) = 10`. It correctly ignores the smaller boundary.
* **Same start times (`[[1, 4], [1, 5]]`):** Sorting places them adjacently. The second interval triggers the overlap condition `1 <= 4`, and `Math.max(4, 5)` updates the end time to `5`. Correct.

No further patches are required. The logic handles these edge cases naturally.

### 8. Analyze expensive sections and optimize

* **Sorting:** `Arrays.sort()` costs $O(n \log n)$ time.
* **Iteration:** We iterate through the array of intervals exactly once, which costs $O(n)$ time.
* **List Operations:** Appending to an `ArrayList` is amortized $O(1)$. Converting it to an array at the end takes $O(n)$ time.
* **Bottleneck:** Sorting is the bottleneck, bringing the total time complexity to $O(n \log n)$. This is theoretically optimal for this problem, as determining overlaps across an unordered set bounds to the same complexity as sorting.
* **Space Complexity:** $O(n)$ space is required to hold the `merged` list (which in the worst case contains $n$ disjoint intervals). The sorting algorithm (typically Dual-Pivot Quicksort for primitives in Java, but Timsort for objects/arrays) will require up to $O(\log n)$ or $O(n)$ auxiliary space.

We do not need to optimize further, as this meets the ideal bounds for this problem.

### Final code

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;

class Solution {
    public int[][] merge(int[][] intervals) {
        if (intervals == null || intervals.length == 0) {
            return new int[0][];
        }

        // Sort intervals based on their start times
        Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));

        List<int[]> merged = new ArrayList<>();
        
        // Start with the first interval
        int[] currentInterval = intervals[0];
        merged.add(currentInterval);
        
        for (int i = 1; i < intervals.length; i++) {
            int[] nextInterval = intervals[i];
            
            // If the next interval starts before or when the current one ends, they overlap
            if (nextInterval[0] <= currentInterval[1]) {
                // Expand the current interval to encompass the next interval
                currentInterval[1] = Math.max(currentInterval[1], nextInterval[1]);
            } else {
                // No overlap. Move to the next interval and add it to our list
                currentInterval = nextInterval;
                merged.add(currentInterval);
            }
        }
        
        // Convert the dynamic list back to a 2D array
        return merged.toArray(new int[0][]);
    }
}

```

### Brief test walkthrough

Let's test with the smallest valid non-trivial input: `[[1, 4], [0, 4]]`.

1. **Input:** `intervals = [[1, 4], [0, 4]]`
2. **Sort:** `Comparator` looks at index `0`. The sorted array becomes `[[0, 4], [1, 4]]`.
3. **Initialization:** `currentInterval = [0, 4]`. `merged` list has `[[0, 4]]`.
4. **Iteration `i = 1`:** `nextInterval = [1, 4]`.
5. **Overlap Check:** `nextInterval[0]` is `1`. `currentInterval[1]` is `4`. Since `1 <= 4`, they overlap.
6. **Merge:** `currentInterval[1] = Math.max(4, 4) = 4`. `currentInterval` remains `[0, 4]`. (Because it was added by reference, the list still reads `[[0, 4]]`).
7. **Return:** `merged.toArray()` produces `[[0, 4]]`.
*Result:* Expected result is produced efficiently.