### question

Given a sorted ascending array with unknown length accessible only via a bounded reader (out‑of‑range returns a sentinel), find the index of a target or return -1

### 1. Restate

Find index of a target value in a sorted array of unknown length. Access array only through `reader.get(k)`. If `k` is out of bounds, returns a sentinel value. Return `-1` if target not found.

### 2. Clarifying Questions

* **Input:** `reader` object, integer `target`.
* **Output:** Integer (index of target or `-1`).
* **Sentinel value:** What is it? (Assume `sys.maxsize` or $\infty$. Safe to treat as strictly greater than any valid target).
* **Duplicates:** Allowed? (Assume yes, return any valid index).

### 3. Example by Hand

Target: `9`. Array: `[-1, 0, 3, 5, 9, 12]` (length unknown).

* Start `left = 0`, `right = 1`.
* `reader.get(1)` is `0`. `0 < 9`.
* Expand: `left = 1`, `right = 2`.
* `reader.get(2)` is `3`. `3 < 9`.
* Expand: `left = 2`, `right = 4`.
* `reader.get(4)` is `9`. `9 >= 9`. Stop expanding.
* Bounds found: `[2, 4]`.
* Binary search in `[2, 4]`:
* `mid = 3`. `reader.get(3)` is `5`. `5 < 9`. Go right.
* `left = 4`, `right = 4`. `mid = 4`. `reader.get(4)` is `9`. Match.


* Return `4`.

### 4. Brainstorming & Complexity

* **Approach A: Linear Scan.** Read `0, 1, 2...` until `val == target` (return index) or `val > target` (return `-1`).
* Time: $O(T)$ where $T$ is target index.
* Space: $O(1)$.


* **Approach B: Exponential Search + Binary Search.** Double the search window to find bounds, then binary search.
* Time: $O(\log T)$. Finding bound takes $\log T$ steps. Binary search takes $\log T$ steps.
* Space: $O(1)$.



### 5. Suggest Solutions

Prefer Approach B. It is logarithmic and scales well for large target indices. Approach A is simpler but fails performance checks for massive arrays. Approach B directly models the manual example from Step 3.

### 6. Outline

```python
def search(reader, target):
    """
    Reframe: Convert unbounded search to bounded binary search via exponential probing.
    State: Left and right index boundaries, chosen because they define a finite search space for binary search.
    Invariant: Target, if present, is strictly >= left boundary and <= right boundary.

    find_bounds(reader, target) = locates a window where target must reside by doubling the right boundary.
    binary_search_window(reader, target, left, right) = standard binary search strictly within known window.

    Core logic:
    - fetch left and right bounds containing target
    - execute binary search within those bounds
    - return target index if found, else negative one

    Edge cases:
    - reader returns sentinel on first read (empty array)
    - target is smaller than first element
    - target not in array
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton (Plain English to stubs)**

```python
def search(reader, target):
    # Core logic outline
    left, right = find_bounds(reader, target)
    return binary_search_window(reader, target, left, right)

```

**Iteration 2: Implementing `find_bounds` (Chunk 1)**

```python
def find_bounds(reader, target):
    left = 0
    right = 1
    # expand bounds exponentially while the value at right pointer is less than target
    while reader.get(right) < target:
        # shift left to current right to save search space
        left = right
        # double right pointer
        right = right * 2
    return left, right

def search(reader, target):
    left, right = find_bounds(reader, target)
    return binary_search_window(reader, target, left, right) # TO DO

```

**Iteration 3: Implementing `binary_search_window` (Chunk 2)**

```python
def binary_search_window(reader, target, left, right):
    while left <= right:
        mid = left + (right - left) // 2
        val = reader.get(mid)
        
        if val == target:
            return mid
        elif val < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return -1

def search(reader, target):
    left, right = find_bounds(reader, target) # DONE
    return binary_search_window(reader, target, left, right) # DONE

```

**Iteration 4: Patching Edge Cases**
Reviewing edge cases from Step 6:

* *Reader returns sentinel immediately / array empty:* Handled. If `get(0)` or `get(1)` is sentinel, sentinel $> \text{target}$, so `while` loop in `find_bounds` breaks immediately. Binary search handles it gracefully.
* *Target smaller than first element:* Handled. `reader.get(1) < target` is false, bounds remain `[0, 1]`, binary search fails to find it and returns `-1`.
* *Sentinel hit during binary search:* Handled. Sentinel value is $\infty$. Condition `val == target` fails. `val < target` fails. Triggers `else` (go left), pulling search correctly back into bounds. No code changes needed. Core logic handles edge cases natively.

Final combined code:

```python
class Solution:
    def search(self, reader: 'ArrayReader', target: int) -> int:
        left, right = 0, 1
        
        # Exponentially expand bounds
        while reader.get(right) < target:
            left = right
            right <<= 1  # multiply by 2
            
        # Standard binary search
        while left <= right:
            mid = left + (right - left) // 2
            val = reader.get(mid)
            
            if val == target:
                return mid
            if val < target:
                left = mid + 1
            else:
                right = mid - 1
                
        return -1

```

### 8. Complexity & Optimizations

* **Time Complexity:** $O(\log T)$ where $T$ is the index of the target. Finding the boundary takes $\log T$ operations. Binary searching the window `[T/2, T]` takes $\log(T - T/2)$ which simplifies to $\log T$ operations.
* **Space Complexity:** $O(1)$. Only pointers maintained.
* **Optimization noted:** In `find_bounds`, instead of `left = 0` continuously, we use `left = right` before doubling. This cuts the binary search space exactly in half, as we know the target is strictly greater than the old `right`. Implemented in the final chunk above. Bitwise shift `right <<= 1` used for minor operation speedup over `right *= 2`.