### question
The median is the middle value in a sorted list of integers. For lists of even length, there is no middle value, so the median is the mean of the two middle values.

For example:

For arr = [1,2,3], the median is 2.
For arr = [1,2], the median is (1 + 2) / 2 = 1.5
Implement the MedianFinder class:

MedianFinder() initializes the MedianFinder object.
void addNum(int num) adds the integer num from the data stream to the data structure.
double findMedian() returns the median of all elements so far.

**1. Restating the question**
Design class to track median of a flowing stream of numbers.
Requires two operations: insert a number, and fetch the current median. Median is middle value (odd count) or average of two middle values (even count).

**2. Clarifying questions, confirming inputs & outputs**

* Inputs: Stream of integers.
* Outputs: `addNum` -> void. `findMedian` -> float/double.
* *Questions:*
* Negative numbers? (Assume yes).
* Duplicates? (Assume yes).
* `findMedian` on empty stream? (Assume invalid, stream will have >= 1 item, or return 0).
* Scale? (Fits in memory).



**3. Example input to output by hand**
Operations: `addNum(1)`, `addNum(2)`, `findMedian()`, `addNum(3)`, `findMedian()`

* `addNum(1)` -> Data: `[1]`
* `addNum(2)` -> Data: `[1, 2]`
* `findMedian()` -> middle of `[1,2]` is `(1+2)/2` -> Returns `1.5`
* `addNum(3)` -> Data: `[1, 2, 3]`
* `findMedian()` -> middle of `[1,2,3]` -> Returns `2.0`

**4. Brainstorming solutions & complexity**

* *Idea 1: Sorted Array.* Append on add, sort array. `addNum`: O(N log N). `findMedian`: O(1).
* *Idea 2: Insertion Sort Array.* Binary search to find index, insert in place. `addNum`: O(N) due to shifting elements. `findMedian`: O(1). (This is the hand-trace method).
* *Idea 3: Two Heaps.* Median only cares about the middle. Split data into two halves: `lower_half` and `upper_half`. Need quick access to largest of `lower_half` and smallest of `upper_half`. Use max-heap for lower, min-heap for upper. `addNum`: O(log N). `findMedian`: O(1).

**5. Suggest solutions**

* Solution A: Keep sorted list, insert element at correct index (Idea 2). Simple to visualize, matches hand trace exactly.
* Solution B: Two Heaps (Idea 3). More efficient. Left side is Max Heap, Right side is Min Heap. Keep sizes balanced.
* *Choice:* Going with Solution B (Two Heaps). O(N) insertion in Solution A is too slow for large streams, but Two Heaps conceptually just splits the hand-traced array down the middle. Preferable and practical.

**6. Outline of selected implementation**

```python
class MedianFinder:
    """
    Reframe: Median only needs access to the middle 1 or 2 elements, not full sorted order.
    State: lower_half (max-heap) and upper_half (min-heap), chosen because heaps give O(1) access to largest/smallest extremes of two partitions.
    Invariant: lower_half size is exactly equal to, or exactly 1 greater than, upper_half size. All elements in lower_half <= all elements in upper_half.

    get_max(lower_half) = returns largest item in lower half
    get_min(upper_half) = returns smallest item in upper half
    push(heap, item) = adds item to appropriate heap
    pop(heap) = removes and returns extreme item from heap

    Core logic:
    - addNum: 
        - add new number to lower_half
        - move the max of lower_half to upper_half to guarantee order
        - if upper_half has more elements than lower_half, move upper_half min back to lower_half to maintain size invariant
    - findMedian:
        - if halves are same size, return average of max(lower_half) and min(upper_half)
        - else, return max(lower_half)
        
    Edge cases:
    - First element insertion (handled smoothly by core logic)
    - Duplicate numbers (heaps handle duplicates naturally)
    - Empty stream median query (deviates from happy path, need safety check)
    """

```

**7. Iterative implementation**

*Iteration 1: Skeleton with dummy helpers*

```python
class MedianFinder:
    def __init__(self):
        self.lower_half = []
        self.upper_half = []

    def addNum(self, num: int) -> None:
        # 1. Add to lower half
        # 2. Move largest of lower to upper
        # 3. Balance sizes
        pass

    def findMedian(self) -> float:
        # Check sizes and return median
        pass

```

*Iteration 2: Translate English core logic to code chunks (ignoring python heap quirks for now)*

```python
class MedianFinder:
    def __init__(self):
        self.lower_half = []
        self.upper_half = []

    def addNum(self, num: int) -> None:
        # Added core logic translation
        self.lower_half.push(num)
        
        largest_lower = self.lower_half.pop()
        self.upper_half.push(largest_lower)
        
        if len(self.upper_half) > len(self.lower_half):
            smallest_upper = self.upper_half.pop()
            self.lower_half.push(smallest_upper)

    def findMedian(self) -> float:
        # Added median calculation
        if len(self.lower_half) == len(self.upper_half):
            return (self.lower_half.get_max() + self.upper_half.get_min()) / 2.0
        else:
            return self.lower_half.get_max()

```

*Iteration 3: Adapt to actual Python structures. Python's `heapq` is a min-heap. Multiply by -1 to simulate max-heap for `lower_half`.*

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.lower_half = [] # max-heap (invert numbers)
        self.upper_half = [] # min-heap (normal numbers)

    def addNum(self, num: int) -> None:
        # Changed push/pop to heapq methods. Invert num for lower_half.
        heapq.heappush(self.lower_half, -num)
        
        # Move max of lower (which is min in inverted heap) to upper
        largest_lower = -heapq.heappop(self.lower_half)
        heapq.heappush(self.upper_half, largest_lower)
        
        # Balance sizes
        if len(self.upper_half) > len(self.lower_half):
            smallest_upper = heapq.heappop(self.upper_half)
            heapq.heappush(self.lower_half, -smallest_upper)

    def findMedian(self) -> float:
        # Adapted get_max / get_min to access heap[0]
        if len(self.lower_half) == len(self.upper_half):
            return (-self.lower_half[0] + self.upper_half[0]) / 2.0
        else:
            return -self.lower_half[0]

```

*Iteration 4: Patching Edge Cases*
Walk the edge case from step 6: "Empty stream median query".

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.lower_half = [] 
        self.upper_half = [] 

    def addNum(self, num: int) -> None:
        heapq.heappush(self.lower_half, -num)
        
        largest_lower = -heapq.heappop(self.lower_half)
        heapq.heappush(self.upper_half, largest_lower)
        
        if len(self.upper_half) > len(self.lower_half):
            smallest_upper = heapq.heappop(self.upper_half)
            heapq.heappush(self.lower_half, -smallest_upper)

    def findMedian(self) -> float:
        # EDGE CASE PATCH: If stream is empty, return 0 to prevent index out of bounds
        if not self.lower_half:
            return 0.0
            
        if len(self.lower_half) == len(self.upper_half):
            return (-self.lower_half[0] + self.upper_half[0]) / 2.0
        else:
            return float(-self.lower_half[0])

```

**8. Complexity & Optimizations**

* **Time Complexity:**
* `addNum`: O(log N). Pushing and popping from heaps takes logarithmic time relative to the number of elements processed.
* `findMedian`: O(1). Accessing the 0th index of a list/heap is constant time.


* **Space Complexity:** O(N) to store all numbers inside the two lists.
* **Optimizations:** The current solution is optimal for general streaming. If bounds are heavily constrained (e.g., numbers strictly between 0 and 100), an array-based frequency counter (bucket sort style) could reduce `addNum` to O(1) and `findMedian` to O(1) by walking buckets up to count/2. Given no constraints, Two Heaps is standard best. Readability is preserved by keeping the push-pop-push flow linear instead of using deeply nested conditionals to peek at values.