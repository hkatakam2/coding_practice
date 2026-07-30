### 1. Restate the problem

We need to determine the minimum number of conference rooms required to accommodate a given list of meeting time intervals. Each interval has a start and end time.

Essentially, we are looking for the maximum number of meetings that overlap at any single point in time. If a meeting starts at the exact same time another meeting ends (e.g., `[0, 8]` and `[8, 10]`), they do not conflict and can safely share the same room.

### 2. Ask clarifying questions

Before writing code, I would confirm a few details about the input and constraints:

* **Input format:** Are the intervals provided as a 2D array of integers (`int[][]`) or a List of custom objects (`List<Interval>`)? *Assumption: I will use `int[][]` where `intervals[i][0]` is the start time and `intervals[i][1]` is the end time, as this is standard in modern Java interviews.*
* **Input size and values:** Can the array be empty? Can times be negative? *Assumption: The array can be empty, and times are non-negative integers representing abstract time blocks.*
* **Sorting:** Is the input guaranteed to be sorted? *Assumption: No, the meetings can be provided in any arbitrary order.*
* **Mutation:** Is it acceptable to modify (sort) the input array directly, or should I create a copy? *Assumption: Sorting the input array in place is acceptable to save memory, as no requirement strictly forbids it.*

### 3. Work through an example by hand

Let's take a representative input that isn't already sorted and has multiple overlaps:
`intervals = [[15, 20], [0, 30], [5, 10]]`

**Step 1: Sort by start time.**
Chronological order makes it easier to process:
`[[0, 30], [5, 10], [15, 20]]`

**Step 2: Process sequentially, tracking when rooms free up.**

* **Meeting 1:** `[0, 30]`
* We have no active meetings.
* Allocate Room A. Room A will be busy until `30`.


* **Meeting 2:** `[5, 10]`
* Meeting 2 starts at `5`. Room A is busy until `30`.
* Since `5 < 30`, we have a conflict.
* Allocate Room B. Room B will be busy until `10`.


* **Meeting 3:** `[15, 20]`
* Meeting 3 starts at `15`.
* Room A is busy until `30`. Room B is busy until `10`.
* Since `15 >= 10`, Room B is now free!
* Assign Meeting 3 to Room B. Room B will now be busy until `20`.



At the end of this process, we used 2 rooms in total.

### 4. Brainstorm solutions aloud

* **Approach 1: Brute Force (Check all overlaps)**
We could compare every meeting against every other meeting to build a graph of conflicts, then try to color the graph. This is incredibly complex to implement correctly under time pressure and completely overkill for interval overlaps.
* **Approach 2: Chronological Sweep-Line**
We can split the intervals into two separate arrays: `startTimes` and `endTimes`. We sort both arrays independently. We then use two pointers to iterate through the timeline. If we encounter a start time before an end time, we increment a `currentRooms` counter. If we encounter an end time, we decrement it. We track the maximum value of `currentRooms`.
*Time:* O(n log n) for sorting. *Space:* O(n) to store the separated arrays.
* **Approach 3: Min-Heap (Priority Queue)**
We sort the intervals by start time. Then, we use a Min-Heap to track the *end times* of currently active meetings. When looking at a new meeting, we compare its start time to the top of the Min-Heap (which represents the earliest ending meeting). If the new meeting starts *after or exactly when* the earliest meeting ends, we pop that meeting from the heap (room is freed). We always push the new meeting's end time onto the heap. The maximum size of the heap during the process (or just the final size, as we only ever replace or add to it) represents the minimum rooms needed.
*Time:* O(n log n). *Space:* O(n).

### 5. Select the solution

I will go with **Approach 3: Min-Heap**.

It perfectly matches the real-world logic of assigning meeting rooms. A `PriorityQueue` in Java is the ideal data structure here because it effortlessly maintains the earliest ending meeting at the top of the heap in `O(log n)` time, saving us from having to manually search for free rooms. While the Sweep-Line approach is also excellent, the Min-Heap approach requires less array manipulation and is very intuitive to explain and trace.

### 6. Write the implementation outline

```java
int minMeetingRooms(int[][] intervals) {
    /*
     * Reframe:
     * Find the maximum simultaneous overlaps of intervals by processing them
     * in chronological order.
     *
     * State:
     * A PriorityQueue (min-heap) tracking the end times of ongoing meetings.
     * Chosen because we repeatedly need the earliest available room (minimum end time).
     *
     * Invariant:
     * The size of the min-heap always reflects the number of distinct rooms 
     * currently allocated. By removing a completed meeting before adding a new one, 
     * we simulate reusing a room.
     *
     * Core logic:
     * - sort the input intervals ascending by their start times
     * - create a PriorityQueue for integers (end times)
     * - add the first meeting's end time to the queue
     * - loop through the remaining meetings:
     *   - if the current meeting starts at or after the earliest ending meeting (queue.peek()),
     *     remove the earliest meeting from the queue
     *   - add the current meeting's end time to the queue
     * - return the size of the queue
     *
     * Edge cases:
     * - null or empty intervals array
     */
}

```

### 7. Implement iteratively

#### Iteration 1: Method skeleton

I'll set up the initial guard clauses, sort the array, and initialize the Priority Queue.

```java
public int minMeetingRooms(int[][] intervals) {
    if (intervals == null || intervals.length == 0) {
        return 0;
    }

    // Sort intervals by start time.
    Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));

    // Min-heap to track the end times of active meetings.
    PriorityQueue<Integer> endTimes = new PriorityQueue<>();

    // TODO: iterate through intervals and manage the heap

    return endTimes.size();
}

```

*I chose `Comparator.comparingInt` rather than `(a, b) -> a[0] - b[0]` to explicitly prevent any theoretical integer overflow, even though times are typically positive.*

#### Iteration 2: Complete the core logic

Now I'll implement the loop to process the sorted intervals and update the heap.

```java
public int minMeetingRooms(int[][] intervals) {
    if (intervals == null || intervals.length == 0) {
        return 0;
    }

    Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));
    PriorityQueue<Integer> endTimes = new PriorityQueue<>();

    // Added: Seed the heap with the first meeting's end time.
    endTimes.offer(intervals[0][1]);

    // Added: Process remaining meetings.
    for (int i = 1; i < intervals.length; i++) {
        int[] currentMeeting = intervals[i];
        
        // If the earliest ending meeting finishes before or exactly when 
        // the current meeting starts, we can reuse that room.
        if (currentMeeting[0] >= endTimes.peek()) {
            endTimes.poll(); // Free up the room
        }
        
        // Allocate a room for the current meeting (either new or reused).
        endTimes.offer(currentMeeting[1]);
    }

    // The size of the heap corresponds to the total rooms allocated.
    return endTimes.size();
}

```

#### Edge-case pass

Let's review the edge cases identified in the outline:

1. **`intervals` is `null` or empty:** Caught cleanly by the initial `if` block, returning `0`.
2. **Only one meeting:** The loop starts at `i = 1`. If `intervals.length == 1`, the loop doesn't execute, and the heap size is correctly `1`.
3. **Meetings with exact same start time:** `Arrays.sort` will place them adjacently. The heap will simply allocate a new room for each until one finishes. Correct.
4. **Adjacency (`start == previousEnd`):** The condition `currentMeeting[0] >= endTimes.peek()` accurately covers this. It will correctly pop the old meeting, indicating room reuse.

The code handles all edge cases without requiring additional patches.

### 8. Analyze expensive sections and optimize

* **Time Complexity:**
* Sorting the intervals array takes O(N log N) time, where N is the number of meetings.
* Iterating through the array takes O(N) steps. Inside the loop, `poll()` and `offer()` on the PriorityQueue take O(log N) time in the worst case (when no rooms are reused). The total cost for the loop is O(N log N).
* **Total Time Complexity:** O(N log N). This is optimally bounded by the sorting step.


* **Space Complexity:**
* The PriorityQueue stores at most N elements (if all meetings overlap).
* Sorting also requires O(log N) to O(N) auxiliary space depending on the internal Java implementation (TimSort).
* **Total Space Complexity:** O(N).



There are no expensive hidden string operations, unnecessary boxing, or heavy object allocations. `PriorityQueue<Integer>` relies on auto-boxing, but given standard interview constraints, this is entirely acceptable and idiomatic Java. A custom array-based heap would avoid boxing but is unnecessarily dense for an interview.

### Final Code

```java
import java.util.Arrays;
import java.util.Comparator;
import java.util.PriorityQueue;

class Solution {
    public int minMeetingRooms(int[][] intervals) {
        if (intervals == null || intervals.length == 0) {
            return 0;
        }

        // Sort intervals based on start time
        Arrays.sort(intervals, Comparator.comparingInt(meeting -> meeting[0]));

        // Min-heap to keep track of the end times of ongoing meetings
        PriorityQueue<Integer> endTimes = new PriorityQueue<>();
        
        // Add the first meeting's end time
        endTimes.offer(intervals[0][1]);

        for (int i = 1; i < intervals.length; i++) {
            int currentStart = intervals[i][0];
            int currentEnd = intervals[i][1];
            
            // If the room that frees up earliest is ready, we reuse it
            if (currentStart >= endTimes.peek()) {
                endTimes.poll();
            }
            
            // Record the current meeting's end time
            endTimes.offer(currentEnd);
        }

        // The number of active elements in the heap is the minimum rooms required
        return endTimes.size();
    }
}

```

### Brief test walkthrough

Let's test with: `intervals = [[0, 8], [8, 10], [5, 9]]`

1. Sort by start: `[[0, 8], [5, 9], [8, 10]]`
2. Initialize heap: `[]`
3. Meeting `[0, 8]`: Heap becomes `[8]`.
4. Meeting `[5, 9]`: `currentStart` (5) < `peek()` (8). Cannot reuse. Heap becomes `[8, 9]`.
5. Meeting `[8, 10]`: `currentStart` (8) >= `peek()` (8). Reuse room! `poll()` removes 8. `offer(10)` adds 10. Heap becomes `[9, 10]`.
6. Loop finishes. Heap size is 2. Returns 2.

The logic accurately identifies that 2 rooms are needed, appropriately handling the adjacent `[0, 8]` and `[8, 10]` sequence.