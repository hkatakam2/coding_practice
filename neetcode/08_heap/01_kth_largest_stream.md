### question
Design a class to find the kth largest integer in a stream of values, including duplicates. E.g. the 2nd largest from [1, 2, 3, 3] is 3. The stream is not necessarily sorted.

Implement the following methods:

constructor(int k, int[] nums) Initializes the object given an integer k and the stream of integers nums.
int add(int val) Adds the integer val to the stream and returns the kth largest integer in the stream.

**1. Restating the Question**
Design a stateful class. It tracks the `k`th largest number in a growing stream of integers. Duplicates count individually.
Class needs:

* `init(k, nums)`: sets up the stream with initial numbers.
* `add(val)`: inserts `val` into the stream, returns the new `k`th largest number.

**2. Clarifying Questions & Confirmations**

* Can `nums` initially have fewer than `k` elements? (Assume yes, `add` might be called until we have `k` elements).
* Are numbers bounded? (Assume standard 32-bit signed integers).
* Does `k` change? (No, fixed at instantiation).
* Input/Output confirmed: `k=3, nums=[4,5,8,2]`. `add(3)` returns `4`.

**3. Hand-trace Example**
Init: `k = 3`, `nums = [4, 5, 8, 2]`
Current top 3: `8, 5, 4`. (Smallest of these is `4`. This is our answer).
Action: `add(3)`
Stream conceptually: `[8, 5, 4, 3, 2]`
Top 3 remain: `8, 5, 4`. Return `4`.
Action: `add(10)`
Stream conceptually: `[10, 8, 5, 4, 3, 2]`
Top 3 become: `10, 8, 5`. Return `5`.

**4. Brainstorming Solutions & Complexity**

* *Approach A: Sort everything on add.* Array stores all numbers. On `add`, append, sort descending, return `arr[k-1]`. Time: $O(N \log N)$ per add. Space: $O(N)$. Slow.
* *Approach B: Maintain sorted array.* On `add`, binary search for position, insert, shift elements. Time: $O(N)$ per add. Space: $O(N)$. Better, but shifting arrays is slow.
* *Approach C: Min-Heap of size K.* If we only care about the top `k` elements, we can discard the rest. A min-heap keeps the smallest element at the top. We store exactly `k` elements. The root is the `k`th largest. Time: $O(\log K)$ per add. Space: $O(K)$.

**5. Suggest Solutions**
Prefer Approach C (Min-Heap). It exactly solves the problem constraints efficiently without tracking useless data. It perfectly matches the hand-trace logic (keeping a "top 3" bucket and returning the smallest of that bucket).

**6. Outline Implementation**

```python
class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        """
        Reframe: The kth largest element in a stream is simply the minimum of the k largest elements seen so far.
        State: A min-heap of size exactly k. Chosen because min-heap provides O(1) access to the minimum and O(log k) updates.
        Invariant: The heap never contains more than k elements.

        push_to_heap(val) = adds value to heap
        pop_from_heap() = removes and returns smallest value from heap
        get_heap_size() = returns current number of elements in heap
        get_heap_min() = peeks at the smallest value in heap without removing

        Core logic:
        - initialize k and an empty min-heap
        - for every number in nums, feed it to the add function
        
        Edge cases:
        - initial nums might have fewer than k elements.
        - stream might currently have fewer than k elements when add() is called.
        """
        pass
        
    def add(self, val: int) -> int:
        """
        Core logic:
        - push new value to the heap
        - if heap size exceeds k, pop the smallest element (which is at the root)
        - return the smallest element currently in the heap
        
        Edge cases:
        - none for the happy path where we already have k elements.
        """
        pass

```

**7. Iterative Implementation**

*Iteration 1: Skeleton with stubs*

```python
import heapq

class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.min_heap = []
        # TODO: process initial nums

    def add(self, val: int) -> int:
        # TODO: add to heap
        # TODO: maintain size k
        # TODO: return kth largest
        pass

```

*Iteration 2: Core logic (Happy path)*

```python
import heapq

class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.min_heap = []
        # Added: loop through initial numbers using our own add method
        for num in nums:
            self.add(num)

    def add(self, val: int) -> int:
        # Added: push to heap
        heapq.heappush(self.min_heap, val)
        
        # Added: maintain size k by popping smallest
        if len(self.min_heap) > self.k:
            heapq.heappop(self.min_heap)
            
        # Added: return the root (smallest of the k largest)
        return self.min_heap[0]

```

*Iteration 3: Edge cases*
Reviewing edge cases from Step 6: What if `add()` is called and we have fewer than `k` elements?
Currently, if `len(min_heap) < self.k`, we don't pop (which is correct), but we `return self.min_heap[0]`. In strict interview settings, returning `None` or raising an error when `< k` elements exist might be required, but usually LeetCode guarantees at least `k` elements exist before returning. No code changes strictly needed for the happy path constraints, but we should acknowledge it.

*Final Core Logic realization is complete.*

**8. Complexity & Optimizations**

*Complexity:*

* **Time:** `init` calls `add` $N$ times. Each `add` takes $O(\log K)$. So `init` is $O(N \log K)$. `add` is $O(\log K)$.
* **Space:** $O(K)$ to store the heap.

*Optimization:*
Instead of calling `add` $N$ times during `init` ($O(N \log K)$), we can optimize the constructor.
We can dump all initial `nums` into the heap, call `heapq.heapify` (which is $O(N)$), and then pop until the size is $k$.

*Optimized Init:*

```python
import heapq

class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.min_heap = nums
        heapq.heapify(self.min_heap) # O(N) time
        
        # Pop smallest elements until we only have k left
        while len(self.min_heap) > self.k:
            heapq.heappop(self.min_heap)

    def add(self, val: int) -> int:
        heapq.heappush(self.min_heap, val)
        if len(self.min_heap) > self.k:
            heapq.heappop(self.min_heap)
            
        return self.min_heap[0]

```

Now `init` is $O(N + (N-K) \log N)$, much faster if $N$ is large. Space remains $O(K)$ effectively (or $O(N)$ temporarily during init depending on how GC handles the reassigned array).