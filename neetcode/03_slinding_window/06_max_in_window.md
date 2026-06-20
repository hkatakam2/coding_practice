### question
You are given an array of integers `nums` and an integer `k`. There is a sliding window of size `k` that starts at the left edge of the array. The window slides one position to the right until it reaches the right edge of the array.
Return a list that contains the maximum element in the window at each step.

# 1. Restate

Window of size `k` slides left→right, one step at a time. At each position, record the max inside the window. Return all those maxes in order.

If `nums` has `n` elements, output has `n - k + 1` values.

# 2. Clarifying questions

- `k` always valid (`1 ≤ k ≤ n`)? Assume yes.
- `nums` empty possible? Assume `n ≥ 1`.
- Negative numbers? Yes, assume full int range.
- Duplicates allowed? Yes.
- Return ints (not indices)? Yes.

# 3. Example by hand

`nums = [1,3,-1,-3,5,3,6,7]`, `k = 3`

```
[1  3 -1] -3  5  3  6  7   → max 3
 1 [3 -1 -3] 5  3  6  7    → max 3
 1  3[-1 -3  5]3  6  7     → max 5
 1  3 -1[-3  5  3]6  7     → max 5
 1  3 -1 -3[ 5  3  6]7     → max 6
 1  3 -1 -3  5[ 3  6  7]   → max 7
```

Output: `[3,3,5,5,6,7]`

# 4. Brainstorm + complexity

**a) Brute force:** for each window, scan all `k` elements for max. `O(n·k)`. Simple, this is literally step 3 by hand.

**b) Max-heap:** push `(val, idx)`, pop stale tops lazily. `O(n log n)`.

**c) Monotonic deque:** keep a deque of indices whose values are decreasing; front is always current max. Each index pushed/popped once → `O(n)`.

Brute force is trivial but slow. Deque is the "right" answer but trickier to reason about. Heap sits in between conceptually.

# 6. Outline

```python
def maxSlidingWindow(nums, k):  # -> list[int]
    """
    Reframe: front of a max-structure = current window max; just lazily
        discard maxes that have slid out of the window.
    State: max-heap of (value, index), chosen because we always want the
        largest value cheaply, and pairing with index lets us know if that
        largest value still lives inside the current window.
    Invariant: heap top is the true window max once all out-of-window
        indices have been evicted from the top.

    push(val, idx)      = add element to heap.
    topMax()            = look at largest value's (value, index).
    isStale(idx, left)  = idx < left, i.e. element sits left of the window.

    Core logic:
    - push the first k elements -> first window full
    - record current max
    - for each new element entering on the right:
        - push it
        - evict any stale top (its index left the window)
        - record current max
    Edge cases:
    - k == 1 -> every element is its own max, output == nums
    - k == n -> single window, one answer
    - duplicates -> fine, indices distinguish them
    - all negatives -> fine, heap orders normally (negate for max-heap)
    """
```

# 7. Iterative implementation

### Skeleton

```python
import heapq

def maxSlidingWindow(nums, k):
    heap = []
    result = []

    # fill first window
    # record first max
    # slide: push new, evict stale top, record max

    return result
```

### Iter 1 — fill first window, record first max (helpers as stubs)

```python
import heapq

def maxSlidingWindow(nums, k):
    heap = []          # max-heap via negated values: (-val, idx)
    result = []

    # fill first window  [0 .. k-1]
    for i in range(k):
        push(heap, nums[i], i)

    result.append(top_max(heap))   # current window max

    # TODO: slide remaining elements
    return result
```

### Iter 2 — implement helpers

```python
import heapq

def push(heap, val, idx):
    heapq.heappush(heap, (-val, idx))   # negate -> max-heap

def top_max(heap):
    return -heap[0][0]                  # undo negation
```

### Iter 3 — the slide (push, evict stale top, record)

```python
def maxSlidingWindow(nums, k):
    heap = []
    result = []

    for i in range(k):                  # first window
        push(heap, nums[i], i)
    result.append(top_max(heap))

    for i in range(k, len(nums)):       # each new right-edge element
        push(heap, nums[i], i)
        left = i - k + 1                # leftmost valid index now
        while heap[0][1] < left:        # top slid out of window -> evict
            heapq.heappop(heap)
        result.append(top_max(heap))

    return result
```

Core logic done. Full:

```python
import heapq

def push(heap, val, idx):
    heapq.heappush(heap, (-val, idx))

def top_max(heap):
    return -heap[0][0]

def maxSlidingWindow(nums, k):  # -> list[int]
    heap, result = [], []

    for i in range(k):
        push(heap, nums[i], i)
    result.append(top_max(heap))

    for i in range(k, len(nums)):
        push(heap, nums[i], i)
        left = i - k + 1
        while heap[0][1] < left:        # discard maxes that left the window
            heapq.heappop(heap)
        result.append(top_max(heap))

    return result
```

### Edge-case walk

- **k == 1**: first loop pushes 1 elem, slide pushes each, top is always current single element. Works, no patch.
- **k == n**: first loop fills everything, second loop never runs, one answer. Works.
- **duplicates**: `(-val, idx)` ties break on idx, eviction still correct. No patch.
- **all negatives**: negation makes most-negative→smallest key correctly. No patch.

No edges break it.

# 8. Complexity

Each element pushed once and popped at most once → heap ops are `O(log n)` each, `O(n log n)` total. Space `O(n)` (heap can hold stale entries until evicted).

Note: only the *top* is evicted when stale, so the heap may carry stale interior entries → worst-case size `n`. That's the cost vs. the `O(n)`-space monotonic deque. If interviewer pushes on space, that's the pivot to deque.

# 6. Outline — Monotonic deque

```python
def maxSlidingWindow(nums, k):  # -> list[int]
    """
    Reframe: keep window's candidates as a decreasing line of indices;
        once a bigger element arrives, every smaller one behind it can
        never be a max again -> drop them. Front = current max.
    State: deque of indices, values strictly decreasing front->back,
        chosen because a smaller element that enters *after* a bigger
        one is permanently dominated (bigger stays in-window at least as
        long), so it's dead weight we can discard immediately.
    Invariant: deque holds only indices still in-window, ordered so their
        values decrease front->back; thus nums[front] is the window max.

    popSmallerBack(val) = drop back indices whose value <= val (dominated).
    popStaleFront(left) = drop front index if it slid out of the window.
    front()             = index of current max.

    Core logic:
    - for each index i as the right edge moves:
        - popSmallerBack: evict back elements <= nums[i] (they're dominated)
        - push i
        - popStaleFront: if front index < window-left, evict it
        - once window is full (i >= k-1), record nums[front]
    Edge cases:
    - k == 1 -> deque always one element, output == nums
    - k == n -> single window recorded at the end
    - duplicates -> using <= on back avoids keeping equal stale dupes;
        (or use < to keep them; either correct, pick one consistently)
    - all negatives -> values still compare normally, no negation needed
    - window not yet full (i < k-1) -> don't record yet
    """
```

# 7. Iterative implementation

### Skeleton

```python
from collections import deque

def maxSlidingWindow(nums, k):
    dq = deque()        # holds indices, values decreasing front->back
    result = []

    for i in range(len(nums)):
        # evict dominated back elements
        # push i
        # evict stale front
        # record max once window full
        pass

    return result
```

### Iter 1 — happy path with helper stubs

```python
from collections import deque

def maxSlidingWindow(nums, k):
    dq, result = deque(), []

    for i in range(len(nums)):
        pop_smaller_back(dq, nums, nums[i])   # drop dominated tails
        dq.append(i)
        pop_stale_front(dq, left=i - k + 1)   # drop front if out of window
        record_max(result, dq, nums, i, k)    # append once full

    return result
```

### Iter 2 — implement back/front eviction helpers

```python
def pop_smaller_back(dq, nums, val):
    while dq and nums[dq[-1]] <= val:   # <= : equal elems dominated too
        dq.pop()

def pop_stale_front(dq, left):
    if dq[0] < left:                    # front slid past window's left edge
        dq.popleft()
```

### Iter 3 — implement record, inline the helpers

```python
from collections import deque

def maxSlidingWindow(nums, k):  # -> list[int]
    dq, result = deque(), []

    for i in range(len(nums)):
        while dq and nums[dq[-1]] <= nums[i]:   # evict dominated tails
            dq.pop()
        dq.append(i)

        if dq[0] < i - k + 1:                   # evict stale front
            dq.popleft()

        if i >= k - 1:                          # window full -> record
            result.append(nums[dq[0]])

    return result
```

Core logic done.

### Edge-case walk

- **k == 1**: back-eviction clears any prior, deque always holds just `i`, `i >= 0` always records → output == nums. Works.
- **k == n**: front never goes stale until the very end; records only at `i == n-1`, one answer. Works.
- **duplicates**: `<=` drops equal values from back, so an older equal index can't linger past its window — front stays valid. Works (using `<` would also work but keep dupes; `<=` is cleaner).
- **all negatives**: plain comparisons, no negation needed. Works.
- **window not full** (`i < k-1`): guarded by `if i >= k-1`, nothing recorded early. Works.

No patches needed — guards already in core.

# 8. Complexity

Each index is appended once and popped at most once (from back or front), so total deque operations are `O(n)` → **time `O(n)`**. Space: deque holds at most `k` indices → **`O(k)`** (vs. heap's `O(n)`).

The single while-loop *looks* nested but is amortized `O(1)` per element — the inner pops are bounded by total pushes. This is the win over the heap: tighter time *and* space, at the cost of the less-obvious "dominated element" insight.