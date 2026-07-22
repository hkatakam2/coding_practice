### 1. Restate the problem

We need to design a data structure that processes a continuous stream of integers and can compute the median of all previously seen integers at any time.

* **Given:** An incoming stream of integers via an `addNum(int num)` method, and a `findMedian()` method to query the median.
* **Returned:** `findMedian()` must return a `double` representing the median.
* **Constraint:** The median is the exact middle value of a sorted sequence. If the number of elements is even, the median is the average of the two middle values.
* **Properties:** Duplicates are allowed. Order of arrival does not dictate the median, but we conceptually need to keep track of the sorted order of the elements.

### 2. Ask clarifying questions

Before implementing, I would clarify a few details:

* **Number of elements:** What is the expected scale of incoming numbers? (Assume up to $10^5$ elements, meaning an $O(n \log n)$ per-insertion or $O(n)$ per-insertion approach will be too slow).
* **Empty query:** Will `findMedian()` ever be called before any numbers are added? (Assume no, or assume it should return 0.0 or throw an exception. We will assume at least one element exists upon calling).
* **Value bounds:** Are there negative values, and can the numbers be extremely large? (Assume standard 32-bit signed integers. Negative numbers are fine, but adding two large integers for the even-length average might cause overflow).
* **Value range:** Is the input strictly bounded (e.g., 0 to 100)? (If it were, we could use an array of frequencies. I will assume no strict bounds, requiring a general-purpose solution).

### 3. Work through an example by hand

Let's trace adding the sequence: `5, 2, 8, 1`.

* **addNum(5)**
* State: `[5]`
* findMedian(): Length is 1 (odd). Middle is `5`. Returns `5.0`.


* **addNum(2)**
* State: sorted is `[2, 5]`
* findMedian(): Length is 2 (even). Average of 2 and 5 is `3.5`. Returns `3.5`.


* **addNum(8)**
* State: sorted is `[2, 5, 8]`
* findMedian(): Length is 3 (odd). Middle is `5`. Returns `5.0`.


* **addNum(1)**
* State: sorted is `[1, 2, 5, 8]`
* findMedian(): Length is 4 (even). Middle values are 2 and 5. Returns `3.5`.



Notice that we never actually need the extreme ends (`1` and `8`) to calculate the median; we only need the highest value of the lower half (`2`) and the lowest value of the upper half (`5`).

### 4. Brainstorm solutions aloud

**Approach 1: Append and Sort**

* **Idea:** Keep an `ArrayList`. Add elements to the list. When `findMedian()` is called, sort the list and return the middle element(s).
* **Complexity:** Insertion is $O(1)$, but finding the median is $O(n \log n)$. If called frequently, this will time out.

**Approach 2: Insertion Sort / Binary Search**

* **Idea:** Maintain a sorted `ArrayList`. For each new number, use binary search to find its correct position in $O(\log n)$ time, then insert it.
* **Complexity:** Finding the median is $O(1)$. However, inserting into the middle of an `ArrayList` requires shifting elements, costing $O(n)$ time per insertion.

**Approach 3: Two Heaps (Max-Heap and Min-Heap)**

* **Idea:** Divide the incoming numbers into two halves. A `lowerHalf` stores the smaller numbers, and an `upperHalf` stores the larger numbers. The median only depends on the boundaries between these halves.
* **Data Structures:**
* A Max-Heap for the `lowerHalf` (so we can quickly access the largest of the small numbers).
* A Min-Heap for the `upperHalf` (so we can quickly access the smallest of the large numbers).


* **Why it works:** By keeping the sizes of the two heaps balanced (differing by at most 1), the median is either the peak of the larger heap, or the average of both peaks.
* **Complexity:** Insertion takes $O(\log n)$ time to push/pop from the heaps. Finding the median takes $O(1)$ time. Space complexity is $O(n)$ to store the numbers.

### 5. Select the solution

I will use the **Two Heaps** approach. It perfectly matches the problem constraints, scaling efficiently to large data streams while satisfying frequent $O(1)$ median queries. We will utilize Java's `PriorityQueue`, which defaults to a min-heap but can easily be configured as a max-heap using `Comparator.reverseOrder()`.

### 6. Write the implementation outline

```java
class MedianFinder {
    /*
     * Reframe:
     * We don't need a fully sorted list; we just need the numbers split at the middle.
     *
     * State:
     * PriorityQueue<Integer> lowerHalf (Max-Heap)
     * PriorityQueue<Integer> upperHalf (Min-Heap)
     * Chosen because PriorityQueues provide O(1) access to extreme values and O(log n) inserts.
     *
     * Invariant:
     * 1. Value separation: Every number in lowerHalf <= every number in upperHalf.
     * 2. Size balance: lowerHalf.size() is equal to upperHalf.size(), OR exactly 1 greater.
     *
     * Core logic (addNum):
     * - Add the new number to lowerHalf.
     * - To maintain the value separation invariant, pop the max from lowerHalf and push it to upperHalf.
     * - To maintain the size balance invariant, if upperHalf is now larger than lowerHalf, 
     *   pop the min from upperHalf and push it back to lowerHalf.
     *
     * Core logic (findMedian):
     * - If lowerHalf has more elements, return its peak.
     * - If sizes are equal, peek both, add them, and divide by 2.0.
     *
     * Edge cases:
     * - Integer overflow when calculating the average of two large integers.
     */
}

```

### 7. Implement iteratively

**Iteration 1: Class skeleton and data structures**
We define the two PriorityQueues and instantiate them.

```java
class MedianFinder {
    private PriorityQueue<Integer> lowerHalf;
    private PriorityQueue<Integer> upperHalf;

    public MedianFinder() {
        // Max-heap requires a reverse order comparator
        lowerHalf = new PriorityQueue<>(Comparator.reverseOrder());
        // Min-heap is the default behavior
        upperHalf = new PriorityQueue<>();
    }

    public void addNum(int num) {
        // TODO: Insert and balance
    }

    public double findMedian() {
        // TODO: Return median based on sizes
        return 0.0;
    }
}

```

**Iteration 2: Implement `findMedian**`
We'll assume the invariants hold true and implement the readout logic.

```java
class MedianFinder {
    private PriorityQueue<Integer> lowerHalf;
    private PriorityQueue<Integer> upperHalf;

    public MedianFinder() {
        lowerHalf = new PriorityQueue<>(Comparator.reverseOrder());
        upperHalf = new PriorityQueue<>();
    }

    public void addNum(int num) {
        // TODO: Insert and balance
    }

    public double findMedian() {
        // Added: Check size invariant. If lowerHalf is larger, the median is an exact element.
        if (lowerHalf.size() > upperHalf.size()) {
            return lowerHalf.peek();
        }
        
        // Added: Sizes are equal, meaning an even total number of elements. 
        // Need to average the two middle values.
        // TODO: prevent integer overflow
        return (lowerHalf.peek() + upperHalf.peek()) / 2.0;
    }
}

```

**Iteration 3: Implement `addNum` and complete the logic**
Now we implement the insertion. We unconditionally push to `lowerHalf`, move the maximum to `upperHalf`, and then correct the sizes. This avoids a messy web of `if/else` checks to determine where the number *should* go.

```java
class MedianFinder {
    private PriorityQueue<Integer> lowerHalf;
    private PriorityQueue<Integer> upperHalf;

    public MedianFinder() {
        lowerHalf = new PriorityQueue<>(Comparator.reverseOrder());
        upperHalf = new PriorityQueue<>();
    }

    public void addNum(int num) {
        // Added: Unconditionally push to lowerHalf
        lowerHalf.offer(num);
        
        // Added: Ensure the highest number in the lower half shifts to the upper half.
        // This guarantees all elements in lowerHalf <= all elements in upperHalf.
        upperHalf.offer(lowerHalf.poll());
        
        // Added: Re-balance sizes. Our invariant states lowerHalf should have >= elements.
        if (upperHalf.size() > lowerHalf.size()) {
            lowerHalf.offer(upperHalf.poll());
        }
    }

    public double findMedian() {
        if (lowerHalf.size() > upperHalf.size()) {
            return lowerHalf.peek();
        }
        
        return (lowerHalf.peek() + upperHalf.peek()) / 2.0;
    }
}

```

**Edge-case pass**

* *Integer Overflow:* If `lowerHalf.peek()` and `upperHalf.peek()` are both close to `Integer.MAX_VALUE`, adding them will overflow into a negative integer before the division by `2.0` casts it to a double.
* *Patch:* Cast one of the peeks to `double` *before* the addition. `(double) lowerHalf.peek() + upperHalf.peek()`.


* *Empty State:* The prompt implies valid calls. If `findMedian()` is called on an empty structure, `peek()` returns null, causing a `NullPointerException` during unboxing to `int`. In a production environment, we should throw an `IllegalStateException`. We will leave it as is per typical interview constraints where `findMedian` is queried only after at least one `addNum`.

### 8. Final Code

```java
import java.util.Comparator;
import java.util.PriorityQueue;

class MedianFinder {
    private PriorityQueue<Integer> lowerHalf;
    private PriorityQueue<Integer> upperHalf;

    public MedianFinder() {
        lowerHalf = new PriorityQueue<>(Comparator.reverseOrder());
        upperHalf = new PriorityQueue<>();
    }

    public void addNum(int num) {
        // Step 1: Add to lower half (Max-Heap)
        lowerHalf.offer(num);
        
        // Step 2: Push the largest element to the upper half (Min-Heap)
        // to maintain the value separation invariant.
        upperHalf.offer(lowerHalf.poll());
        
        // Step 3: Maintain size invariant where lowerHalf is allowed to be larger by 1.
        if (upperHalf.size() > lowerHalf.size()) {
            lowerHalf.offer(upperHalf.poll());
        }
    }

    public double findMedian() {
        if (lowerHalf.size() > upperHalf.size()) {
            return lowerHalf.peek();
        }
        
        // Cast to double prior to addition to prevent 32-bit integer overflow.
        return ((double) lowerHalf.peek() + upperHalf.peek()) / 2.0;
    }
}

```

### 9. Complexity

* **Time Complexity:**
* `addNum`: $O(\log n)$. `offer()` and `poll()` on a `PriorityQueue` require logarithmic time relative to the number of elements in the heap. At worst, we do 3 heap operations per insertion.
* `findMedian`: $O(1)$. `peek()` is a constant-time operation.


* **Space Complexity:** $O(n)$, where $n$ is the total number of elements added to the stream. Both priority queues combined will store exactly $n$ elements.

### 10. Brief test walkthrough

Let's run the extreme case where overflow might occur: adding `2,000,000,000` and `2,000,000,000`.

1. `addNum(2000000000)`: `lowerHalf` gets the value, moves it to `upperHalf`, `upperHalf` becomes larger, moves it back to `lowerHalf`. `lowerHalf` holds `[2000000000]`.
2. `addNum(2000000000)`: `lowerHalf` receives second value. Max moves to `upperHalf`. Size is balanced (1 each).
3. `findMedian()`: Sizes are equal. We calculate `((double) 2000000000 + 2000000000) / 2.0`. The cast immediately promotes the math to 64-bit floating point, bypassing the 32-bit ceiling `2,147,483,647`. Expected result: `2000000000.0`. Validated.