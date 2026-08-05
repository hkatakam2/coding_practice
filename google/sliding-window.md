The Sliding Window
The Setup: A story-based sliding window problem with follow-ups for queries, modified states, and circular arrays. (A user in the comments hinted at the "footpath paint" problem).

### question
Painting the Footpath: A city has a footpath represented by an array of 0s (unpainted) and 1s (painted). The city gives you a single bucket of paint that can paint exactly a contiguous block of $K$ unpainted tiles. If you use your bucket optimally, what is the maximum number of consecutive painted tiles (1s) you can achieve on the footpath? (Expected approach: Fixed-size sliding window of size $K$ to find the segment with the most 0s, or a variable window tracking at most $K$ zeros).


### 1. Restate Question

Given binary array `tiles` where `0` = unpainted and `1` = painted, plus integer `K`. Paint up to `K` unpainted tiles (`0`s $\rightarrow$ `1`s). Find maximum consecutive `1`s achievable in array.

---

### 2. Clarifying Questions & Assumptions

* **Can $K$ exceed total zeros?** Yes. Return `len(tiles)`.
* **Can $K = 0$?** Yes. Return length of longest existing block of `1`s.
* **Can `tiles` be empty?** Assume $N \ge 0$. If empty, return `0`.
* **In-place modification required?** No, compute max length only.
* **Types:** `tiles: list[int]`, `k: int` $\rightarrow$ `returnType: int`.

---

### 3. Hand Trace Example

`tiles = [1, 1, 0, 0, 0, 1, 1, 0, 1, 1]`, `k = 2`

```text
Idx:  0  1  2  3  4  5  6  7  8  9
Val: [1, 1, 0, 0, 0, 1, 1, 0, 1, 1]

R=0..1: [1, 1]          -> zeros=0 <= 2 | max_len = 2
R=2:    [1, 1, 0]       -> zeros=1 <= 2 | max_len = 3
R=3:    [1, 1, 0, 0]    -> zeros=2 <= 2 | max_len = 4
R=4:    [1, 1, 0, 0, 0] -> zeros=3 > 2  | shrink L past idx 2 -> L=3 -> [0, 0] (zeros=2)
R=5..6: [0, 0, 1, 1]    -> zeros=2 <= 2 | max_len = 4
R=7:    [0, 0, 1, 1, 0] -> zeros=3 > 2  | shrink L past idx 3 -> L=4 -> [0, 1, 1, 0] (zeros=2)
R=8:    [0, 1, 1, 0, 1] -> zeros=2 <= 2 | max_len = 5
R=9:    [0, 1, 1, 0, 1, 1] -> zeros=2 <= 2 | max_len = 6

Result: 6

```

---

### 4. Brainstorming Solutions

1. **Brute Force**: Check all subarrays $[i \dots j]$. Count zeros. If zeros $\le K$, track max length $(j - i + 1)$.
* *Time:* $O(N^2)$ | *Space:* $O(1)$


2. **Sliding Window (Two Pointers)**: Expand right end. Maintain window $[L \dots R]$ containing at most $K$ zeros. Shrink left end when zeros $> K$.
* *Time:* $O(N)$ | *Space:* $O(1)$



---

### 5. Selected Solution

**Sliding Window (Two Pointers)**. Linear sweep, minimal tracking state, direct mapping to problem invariant.

---

### 6. Implementation Outline

```python
def max_consecutive_ones(tiles: list[int], k: int) -> int:
    """
    Reframe: Find longest subarray containing at most K zeros.
    State: Left/right boundary pointers, zero counter. Chosen because contiguous window state moves monotonically left-to-right.
    Invariant: Window [left..right] contains at most K zeros after shrinking.

    is_unpainted(tile) = returns True if tile value is 0.

    Core logic:
    - Expand right boundary across array element by element
    - If incoming tile unpainted, increment zero count
    - While zero count exceeds K, advance left boundary and decrement zero count if left tile unpainted
    - Update max window length seen so far
    Edge cases:
    - empty array (returns 0)
    - K >= total zeros (returns array length)
    - K == 0 (returns longest streak of existing 1s)
    """

```

---

### 7. Iterative Code Implementation

#### Step 7.1: Initial Skeleton with Stubs

```python
def max_consecutive_ones(tiles: list[int], k: int) -> int:
    # Helper dummy stub
    def is_unpainted(tile):
        return tile == 0

    left = 0
    zero_count = 0
    max_len = 0

    # Core Loop Skeleton
    for right in range(len(tiles)):
        # TODO: update zero_count for incoming right tile
        # TODO: shrink window from left if zero_count > k
        # TODO: update max_len
        pass

    return max_len

```

#### Step 7.2: Build Core Logic (Expanding Right & Shrinking Left)

```python
def max_consecutive_ones(tiles: list[int], k: int) -> int:
    def is_unpainted(tile):
        return tile == 0

    left = 0
    zero_count = 0
    max_len = 0

    for right in range(len(tiles)):
        # Iteration 1: Expand right & track zeros
        if is_unpainted(tiles[right]):
            zero_count += 1
            
        # Iteration 2: Shrink left while invariant violated
        while zero_count > k:
            if is_unpainted(tiles[left]):
                zero_count -= 1
            left += 1

        # Iteration 3: Track max valid window length
        current_len = right - left + 1
        if current_len > max_len:
            max_len = current_len

    return max_len

```

#### Step 7.3: Clean Up Helpers into Idiomatic Python & Walk Edge Cases

Walk edge cases identified in Step 6:

1. **Empty Array (`tiles = []`)**: Loop doesn't run, returns `max_len = 0`. Correct.
2. **$K \ge \text{zeros}$**: `while zero_count > k` never triggers. Returns `len(tiles)`. Correct.
3. **$K = 0$**: `while zero_count > 0` triggers whenever `tiles[right] == 0`, moving `left` past zero. Measures max streak of `1`s. Correct.

```python
def max_consecutive_ones(tiles: list[int], k: int) -> int:
    left = 0
    zero_count = 0
    max_len = 0

    for right in range(len(tiles)):
        if tiles[right] == 0:
            zero_count += 1
            
        while zero_count > k:
            if tiles[left] == 0:
                zero_count -= 1
            left += 1

        max_len = max(max_len, right - left + 1)

    return max_len

```

---

### 8. Complexity & Optimization Commentary

* **Time Complexity:** $\mathcal{O}(N)$. Each index visited by `right` once and `left` at most once.
* **Space Complexity:** $\mathcal{O}(1)$. Constant extra variables.

#### Optional Non-Shrinking Window Optimization

Instead of shrinking window with `while`, replace with `if`. Window size never decreases, saving redundant operations:

```python
def max_consecutive_ones_optimized(tiles: list[int], k: int) -> int:
    left = 0
    zero_count = 0

    for right in range(len(tiles)):
        if tiles[right] == 0:
            zero_count += 1
            
        # If invalid, shift entire window right without shrinking max size achieved
        if zero_count > k:
            if tiles[left] == 0:
                zero_count -= 1
            left += 1

    return len(tiles) - left

```
### follow up1
Circular Footpath: It turns out this footpath wraps entirely around a circular city park. The end of the array connects back to the beginning. How does your sliding window approach change to account for this circular nature? (Expected approach: Concatenate the array with itself nums + nums or use modulo arithmetic for the window pointers).

### 1. Restate Question

Given binary array `tiles` representing circular footpath (`0` = unpainted, `1` = painted) and integer `K` (paint bucket capacity). End of array connects back to start. Paint up to `K` unpainted tiles to achieve max consecutive `1`s. Single tile cannot be counted twice (max possible length is array length $N$).

---

### 2. Confirm Inputs, Outputs & Clarifying Questions

* **Inputs:** `tiles: list[int]`, `k: int`
* **Output:** `int` (max consecutive painted tiles)
* **Can window wrap around multiple times?** No, window length capped at $N = \text{len}(\text{tiles})$.
* **What if $K \ge$ total `0`s?** Return $N$.
* **What if `tiles` is empty?** Return `0`.

---

### 3. Hand Trace Example

`tiles = [0, 1, 1, 0]`, `k = 1`, $N = 4$
Concatenated array (length $2N = 8$): `[0, 1, 1, 0, 0, 1, 1, 0]`
Constraint: `zeros <= 1` AND `len <= 4`

```text
Idx:  0  1  2  3  4  5  6  7
Val: [0, 1, 1, 0, 0, 1, 1, 0]

R=0: [0]          -> zeros=1 <= 1, len=1 <= 4 | max_len = 1
R=1: [0, 1]       -> zeros=1 <= 1, len=2 <= 4 | max_len = 2
R=2: [0, 1, 1]    -> zeros=1 <= 1, len=3 <= 4 | max_len = 3
R=3: [0, 1, 1, 0] -> zeros=2 > 1              | shrink L -> L=1 -> [1, 1, 0] (zeros=1, len=3)
R=4: [1, 1, 0, 0] -> zeros=2 > 1              | shrink L twice -> L=3 -> [0, 0] -> L=4 -> [0] (len=1)
R=5: [0, 1]       -> zeros=1 <= 1, len=2 <= 4 | max_len = 3
R=6: [0, 1, 1]    -> zeros=1 <= 1, len=3 <= 4 | max_len = 3
R=7: [0, 1, 1, 0] -> zeros=2 > 1              | shrink L -> [1, 1, 0] (len=3)

Result: 3

```

---

### 4. Brainstorming Solutions

1. **Brute Force (Circular)**: Check all subarrays starting at every index $i$ up to length $N$.
* *Time:* $\mathcal{O}(N^2)$ | *Space:* $\mathcal{O}(1)$


2. **Concatenation + Sliding Window**: Double array (`tiles + tiles`). Run sliding window capped at max size $N$ with max $K$ zeros.
* *Time:* $\mathcal{O}(N)$ | *Space:* $\mathcal{O}(N)$


3. **Modulo Sliding Window**: Same logic as concatenation, using `i % N` virtual indexing over `2 * N` range.
* *Time:* $\mathcal{O}(N)$ | *Space:* $\mathcal{O}(1)$



---

### 5. Suggested Solution

**Concatenation + Sliding Window**. Explicitly duplicating array makes boundary wrap-around logic intuitive and reduces bug surface area compared to complex modulo pointer boundary conditions.

---

### 6. Outline of Implementation

```python
def max_consecutive_ones_circular(tiles: list[int], k: int) -> int: # -> int
    """
    Reframe: Find longest valid subarray in duplicated array, capped at length N with at most K zeros.
    State: Left pointer, right pointer, zero count in current window. Chosen because contiguous sliding window properties hold across concatenated array.
    Invariant: Window [left..right] has zero count <= K AND window length <= N after shrinking.

    is_unpainted(tile) = returns True if tile value is 0.
    is_window_too_large(left, right, max_len) = returns True if window size strictly exceeds max_len.

    Core logic:
    - Double tiles array to handle circular overlap seamlessly
    - Expand right boundary through doubled array
    - Increment zero count if incoming tile unpainted
    - While zero count exceeds K OR window length exceeds N, shrink from left and update zero count
    - Track maximum valid window length seen
    Edge cases:
    - Empty tiles array
    - K exceeds or equals total zeros in array
    - K = 0 (no paint available)
    """

```

---

### 7. Iterative Implementation

#### Step 7.1: Skeleton with Plain English Logic & Stubs

```python
def max_consecutive_ones_circular(tiles: list[int], k: int) -> int:
    def is_unpainted(tile):
        return tile == 0

    def is_window_too_large(left, right, max_allowed):
        return (right - left + 1) > max_allowed

    # TODO: Handle array concatenation
    left = 0
    zero_count = 0
    max_len = 0

    # Core Loop Skeleton
    # TODO: iterate right pointer through concatenated array
        # TODO: track zero count
        # TODO: shrink left while zero_count > k OR window size > N
        # TODO: update max_len

    return max_len

```

#### Step 7.2: Build Core Logic (Concatenation & Window Expansion)

```python
def max_consecutive_ones_circular(tiles: list[int], k: int) -> int:
    def is_unpainted(tile):
        return tile == 0

    def is_window_too_large(left, right, max_allowed):
        return (right - left + 1) > max_allowed

    n = len(tiles)
    extended_tiles = tiles + tiles  # Added: Double array for circular sweep
    
    left = 0
    zero_count = 0
    max_len = 0

    for right in range(len(extended_tiles)):  # Added: Sweep across extended array
        if is_unpainted(extended_tiles[right]):  # Added: Track incoming zero
            zero_count += 1

        # Added: Shrink window if zero budget exceeded OR length exceeds N
        while zero_count > k or is_window_too_large(left, right, n):
            if is_unpainted(extended_tiles[left]):
                zero_count -= 1
            left += 1

        max_len = max(max_len, right - left + 1)  # Added: Track max length

    return max_len

```

#### Step 7.3: Clean Up Logic into Idiomatic Python

```python
def max_consecutive_ones_circular(tiles: list[int], k: int) -> int:
    if not tiles:
        return 0

    n = len(tiles)
    extended_tiles = tiles + tiles
    
    left = 0
    zero_count = 0
    max_len = 0

    for right in range(len(extended_tiles)):
        if extended_tiles[right] == 0:
            zero_count += 1

        while zero_count > k or (right - left + 1) > n:
            if extended_tiles[left] == 0:
                zero_count -= 1
            left += 1

        max_len = max(max_len, right - left + 1)

    return max_len

```

#### Step 7.4: Walk Edge Cases & Patch

1. **Empty Array (`tiles = []`)**: Handled explicitly by `if not tiles: return 0`.
2. **$K \ge$ Total Zeros**: `zero_count > k` never fires for zero constraint. `right - left + 1 > n` fires as soon as window reaches $N+1$, maintaining `max_len = N`. Correct.
3. **$K = 0$**: Window shrinks whenever `extended_tiles[right] == 0`. Max length of continuous `1`s capped at $N$. Correct.

---

### 8. Complexity & Space Optimization

* **Current Implementation Complexity:**
* **Time:** $\mathcal{O}(N)$ - Loop runs $2N$ iterations. Pointers advance monotonically.
* **Space:** $\mathcal{O}(N)$ - Allocation of `extended_tiles`.



#### $\mathcal{O}(1)$ Auxiliary Space Optimization (Virtual Indexing)

Avoid allocating extra space by using modulo arithmetic `right % N` and `left % N`:

```python
def max_consecutive_ones_circular_optimized(tiles: list[int], k: int) -> int:
    if not tiles:
        return 0

    n = len(tiles)
    left = 0
    zero_count = 0
    max_len = 0

    for right in range(2 * n):
        if tiles[right % n] == 0:
            zero_count += 1

        while zero_count > k or (right - left + 1) > n:
            if tiles[left % n] == 0:
                zero_count -= 1
            left += 1

        max_len = max(max_len, right - left + 1)

    return max_len

```

### follow up 2
Query-Based Budgets: Instead of a single bucket of size $K$, the city council is proposing different budget plans. You are given an array of queries Q, where each Q[i] represents a different bucket capacity $K$. Return an array of the maximum consecutive painted tiles for each query. (Expected approach: Precompute prefix sums of 0s and use binary search, or a two-pointer approach for each query).

### 1. Restating the Question

Given binary array `tiles` (`0` = unpainted, `1` = painted) and query array `Q` where each element represents bucket capacity $K$ (max `0`s turnable into `1`s). For each query $Q[i]$, find max consecutive `1`s achievable on footpath. Return array of max lengths corresponding to `Q`.

---

### 2. Clarifying Questions & Confirming Inputs/Outputs

* **Inputs:** `tiles: list[int]`, `Q: list[int]`
* **Outputs:** `list[int]` where $i$-th element is answer for capacity $Q[i]$.
* **Can $K$ exceed total zeros in `tiles`?** Yes. Max consecutive `1`s capped at $N = \text{len}(tiles)$.
* **Can $K = 0$?** Yes. Returns max existing streak of `1`s.
* **Can `tiles` or `Q` be empty?** If `tiles` empty, return `0` for all queries. If `Q` empty, return `[]`.
* **Are values guaranteed $0$ and $1$?** Yes.

---

### 3. Hand Trace Example

`tiles = [1, 1, 0, 0, 0, 1, 1, 0, 1, 1]` ($N = 10$)

`Q = [1, 2, 0, 5]`

```text
Query K = 1:
- Window [0..1]: [1, 1]                (zeros=0 <= 1) -> len=2
- Window [0..2]: [1, 1, 0]             (zeros=1 <= 1) -> len=3
- Window [0..3]: [1, 1, 0, 0]          (zeros=2 > 1)  -> shrink L to 3 -> [0] (zeros=1) -> len=1
- Window [4..9]: [0, 1, 1, 0, 1, 1]    (zeros=2 > 1)  -> shrink L to 5 -> [1, 1, 0, 1, 1] (zeros=1) -> len=5
Result for K=1: 5

Query K = 2:
- Window [0..3]: [1, 1, 0, 0]          (zeros=2 <= 2) -> len=4
- Window [4..9]: [0, 1, 1, 0, 1, 1]    (zeros=2 <= 2) -> len=6
Result for K=2: 6

Query K = 0:
- Max existing streak of 1s without flipping zeros -> idx 0..1 or 5..6 or 8..9.
Result for K=0: 2

Query K = 5:
- Total zeros = 4. K >= 4 flips all zeros to ones -> entire array length.
Result for K=5: 10

Final Output: [5, 6, 2, 10]

```

---

### 4. Brainstorming Solutions & Complexity

1. **Per-Query Sliding Window**:
For each capacity $K \in Q$, run two-pointer sliding window to find longest subarray with $\le K$ zeros.
* *Time:* $O(M \times N)$ where $N = \text{len}(tiles)$, $M = \text{len}(Q)$.
* *Space:* $O(1)$ auxiliary (excluding output array).


2. **Prefix Sum + Binary Search**:
Precompute zero count prefix array `zero_prefix`. For each query $K$, iterate start index $i \in [0, N-1]$, binary search max end index $j$ where `zero_prefix[j+1] - zero_prefix[i] <= K`.
* *Time:* $O(N + M \times N \log N)$.
* *Space:* $O(N)$ auxiliary.


3. **Precalculated Zero Indices + Binary Search**:
Store indices of all zeros. For each query $K$, check gap between index $p$ and index $p + K + 1$ in zero index array.
* *Time:* $O(N + M \log Z)$ where $Z$ is zero count.
* *Space:* $O(Z)$.



---

### 5. Suggested Solution

**Per-Query Sliding Window (Solution 1)**. Most straightforward, zero precomputation overhead, intuitive logic, optimal $O(1)$ auxiliary space.

---

### 6. Outline of Selected Implementation

```python
def max_consecutive_ones_queries(tiles: list[int], Q: list[int]) -> list[int]:
    """
    Reframe: For each query capacity K, find max length subarray with at most K zeros.
    State: Left/right boundary pointers and zero counter per query, chosen because window moves monotonically left-to-right across tiles.
    Invariant: Active window [left..right] contains at most K zeros.

    is_unpainted(tile) = returns True if tile value is 0.

    Core logic:
    - initialize empty results list
    - for each query capacity K in Q:
      - reset window left pointer, zero counter, max length
      - for each right index in tiles:
        - if incoming right tile unpainted, increment zero counter
        - while zero counter exceeds K, advance left pointer and decrement zero counter if left tile unpainted
        - update max window length for capacity K
      - append max length to results list
    - return results list

    Edge cases:
    - empty tiles array
    - empty queries array
    - capacity K exceeds total zeros in tiles
    - capacity K is zero
    """

```

---

### 7. Iterative Implementation

#### Step 7.1: Skeleton with Placeholders & Helper Stubs

```python
def max_consecutive_ones_queries(tiles: list[int], Q: list[int]) -> list[int]:
    def is_unpainted(tile):
        return tile == 0

    results = []

    for k in Q:
        # TODO: run sliding window logic for capacity k
        # TODO: track max length for k
        # TODO: append max length to results
        pass

    return results

```

#### Step 7.2: Build Core Logic Iteration 1 (Sliding Window for Single Query)

```python
def max_consecutive_ones_queries(tiles: list[int], Q: list[int]) -> list[int]:
    def is_unpainted(tile):
        return tile == 0

    results = []

    for k in Q:
        left = 0
        zero_count = 0
        max_len = 0

        # Iteration 1: Expand right boundary & update zero count
        for right in range(len(tiles)):
            if is_unpainted(tiles[right]):
                zero_count += 1

            # Iteration 2: Shrink window from left if zero count > k
            while zero_count > k:
                if is_unpainted(tiles[left]):
                    zero_count -= 1
                left += 1

            # Iteration 3: Track max length seen for capacity k
            current_len = right - left + 1
            if current_len > max_len:
                max_len = current_len

        results.append(max_len)

    return results

```

#### Step 7.3: Inline Optimization & Idiomatic Python

```python
def max_consecutive_ones_queries(tiles: list[int], Q: list[int]) -> list[int]:
    results = []

    for k in Q:
        left = 0
        zero_count = 0
        max_len = 0

        for right in range(len(tiles)):
            # Direct check replacing helper fn for simplicity
            if tiles[right] == 0:
                zero_count += 1

            while zero_count > k:
                if tiles[left] == 0:
                    zero_count -= 1
                left += 1

            max_len = max(max_len, right - left + 1)

        results.append(max_len)

    return results

```

#### Step 7.4: Edge Case Verification & Patching

Walk edge cases listed in Step 6:

1. **Empty `tiles` (`tiles = []`)**: Outer loop runs per query, inner `range(len(tiles))` is empty, `max_len = 0` appended for each query. Correct.
2. **Empty `Q` (`Q = []`)**: Returns `[]`. Correct.
3. **Capacity $K \ge \text{total zeros}$**: `while zero_count > k` never executes, `max_len` reaches `len(tiles)`. Correct.
4. **Capacity $K = 0$**: `while zero_count > 0` triggers on every `0`, pushing `left` past `right`, tracking max existing block of `1`s. Correct.

*No additional code patching needed; happy path naturally handles all identified edge cases.*

---

### 8. Complexity & Optimization Commentary

```python
# Expensive section: Nested loops (outer Q, inner tiles)
# Outer loop executes M times (len(Q)), Inner loop moves pointers N times (len(tiles))
# Overall Time Complexity: O(M * N)
# Auxiliary Space Complexity: O(1) (excluding returned results array of size M)

```

#### Optimization for Large $M$ (Many Queries):

If $M$ is large ($M \gg N$), precompute indices of `0`s to process queries in $O(\log N)$ each:

```python
import bisect

def max_consecutive_ones_queries_optimized(tiles: list[int], Q: list[int]) -> list[int]:
    # Store 0-indexed positions of all 0s, with boundary sentinels
    zero_indices = [-1] + [i for i, tile in enumerate(tiles) if tile == 0] + [len(tiles)]
    total_zeros = len(zero_indices) - 2

    results = []
    for k in Q:
        if k >= total_zeros:
            results.append(len(tiles))
            continue
        
        # Max distance across (k + 1) zeros
        max_len = 0
        for i in range(len(zero_indices) - (k + 1)):
            length = zero_indices[i + k + 1] - zero_indices[i] - 1
            max_len = max(max_len, length)
            
        results.append(max_len)

    return results

```

* **Precomputation Time:** $O(N)$
* **Per Query Time:** $O(Z)$ where $Z$ = number of zeros ($Z \le N$)
* **Total Space:** $O(Z)$ for zero index array

### follow up 3
### 1. Restate Question

Footpath represented by binary array `tiles` (0 = unpainted, 1 = painted).
Support stream of dynamic operations:

* `update(index, value)`: change `tiles[index]` to `0` or `1`.
* `query(k)`: find maximum consecutive painted tiles possible by painting at most `k` unpainted tiles under current state.

---

### 2. Clarifying Questions & Confirming Inputs/Outputs

* **Operation counts & bounds:** Assume array length $N \le 10^5$, operations $Q \le 10^5$.
* **Valid updates:** `index` within `[0, N-1]`, `value` $\in \{0, 1\}$.
* **Value of $K$:** Can $k \ge \text{total unpainted tiles}$? Yes, return $N$. Can $k = 0$? Yes, return length of longest existing block of `1`s.
* **Interface:** Object state with `update(index, value)` returning `None` and `query(k)` returning `int`.

---

### 3. Hand Trace Example

```text
Initial: tiles = [1, 0, 1, 0, 1]

1. query(k = 1):
   Unpainted tiles at indices 1, 3.
   - Paint idx 1 -> [1, 1, 1, 0, 1] -> max consecutive 1s = 3
   - Paint idx 3 -> [1, 0, 1, 1, 1] -> max consecutive 1s = 3
   Output: 3

2. update(index = 1, value = 1):
   tiles becomes [1, 1, 1, 0, 1]

3. query(k = 1):
   Unpainted tile at index 3.
   - Paint idx 3 -> [1, 1, 1, 1, 1] -> max consecutive 1s = 5
   Output: 5

```

---

### 4. Brainstorming Solutions & Complexity

1. **Plain Array + Two-Pointer Sliding Window per Query**:
* `update`: direct mutation `tiles[idx] = val`.
* `query`: run standard sliding window across array.
* *Time:* Update $\mathcal{O}(1)$, Query $\mathcal{O}(N)$ | *Space:* $\mathcal{O}(N)$


2. **Fenwick Tree (Binary Indexed Tree) for Zero Counts + Two Pointers**:
* Store `1` at index $i$ if `tiles[i] == 0`, else `0`.
* `update`: point update in Fenwick Tree.
* `query`: two-pointer sliding window using prefix sums from Fenwick Tree.
* *Time:* Update $\mathcal{O}(\log N)$, Query $\mathcal{O}(N \log N)$ | *Space:* $\mathcal{O}(N)$


3. **Segment Tree with Tree Walk**:
* Segment tree nodes maintain count of zeros.
* `update`: point update in tree.
* `query`: walk tree or binary search right endpoint.
* *Time:* Update $\mathcal{O}(\log N)$, Query $\mathcal{O}(N \log N)$ | *Space:* $\mathcal{O}(N)$



---

### 5. Suggest Solutions

Suggest **Option 2 (Fenwick Tree / Binary Indexed Tree + Two Pointers)**.

* Simple $\mathcal{O}(N)$ array representation.
* Clean $\mathcal{O}(\log N)$ point updates.
* Easy to explain, robust against off-by-one errors compared to node-merging Segment Trees.

---

### 6. Outline of Selected Implementation

```python
def query(self, k: int) -> int:
    """
    Reframe: Find max window [left..right] where count of 0s <= k under dynamic updates.
    State: Fenwick Tree (Binary Indexed Tree) storing 1 if tile is 0, else 0.
           Chosen because BIT provides O(log N) point updates and prefix sum range queries.
    Invariant: Range sum from left to right in BIT equals exact count of unpainted tiles (0s) in tiles[left..right].

    get_zeros(left, right) = returns count of 0s in range [left..right] via BIT range sum query.

    Core logic:
    - initialize left boundary to zero and max length tracker to zero
    - expand right boundary across all tiles
    - while count of zeros in range left to right exceeds k, advance left boundary
    - update max length seen so far
    Edge cases:
    - k >= total zeros (returns full array length)
    - k == 0 (returns longest streak of existing 1s)
    - index out of bounds on update
    - redundant update (value matches current tile)
    """

```

---

### 7. Iterative Implementation

#### Step 7.1: Skeleton with Stubs

```python
class FenwickTree:
    def __init__(self, size: int):
        self.tree = [0] * (size + 1)

    def add(self, idx: int, delta: int) -> None:
        # TODO: Implement BIT point update
        pass

    def query(self, idx: int) -> int:
        # TODO: Implement BIT prefix sum query
        return 0


class DynamicFootpath:
    def __init__(self, tiles: list[int]):
        self.tiles = list(tiles)
        self.bit = FenwickTree(len(tiles))
        # TODO: Initialize BIT with initial zero positions

    def update(self, index: int, value: int) -> None:
        # TODO: Handle tile updates and update BIT
        pass

    def query(self, k: int) -> int:
        def get_zeros(left: int, right: int) -> int:
            # Dummy aid helper stub
            return 0

        left = 0
        max_len = 0

        for right in range(len(self.tiles)):
            # TODO: shrink window from left using get_zeros helper
            # TODO: update max_len
            pass

        return max_len

```

#### Step 7.2: Building Core Logic (BIT Implementation & Query Loop)

```python
class FenwickTree:
    def __init__(self, size: int):
        self.tree = [0] * (size + 1)

    def add(self, idx: int, delta: int) -> None:
        idx += 1  # 1-based indexing for BIT
        while idx < len(self.tree):
            self.tree[idx] += delta
            idx += idx & (-idx)

    def query(self, idx: int) -> int:
        idx += 1  # 1-based indexing for BIT
        total = 0
        while idx > 0:
            total += self.tree[idx]
            idx -= idx & (-idx)
        return total


class DynamicFootpath:
    def __init__(self, tiles: list[int]):
        self.tiles = list(tiles)
        self.bit = FenwickTree(len(tiles))
        # Added: populate BIT (1 if unpainted/0, else 0)
        for i, val in enumerate(self.tiles):
            if val == 0:
                self.bit.add(i, 1)

    def update(self, index: int, value: int) -> None:
        # Added: compute delta and update array + BIT
        if self.tiles[index] == value:
            return
        
        delta = 1 if value == 0 else -1
        self.bit.add(index, delta)
        self.tiles[index] = value

    def query(self, k: int) -> int:
        def get_zeros(left: int, right: int) -> int:
            # Added: actual BIT range query logic
            if left > right:
                return 0
            left_sum = self.bit.query(left - 1) if left > 0 else 0
            return self.bit.query(right) - left_sum

        left = 0
        max_len = 0

        for right in range(len(self.tiles)):
            # Added: core two-pointer expansion and shrinking
            while get_zeros(left, right) > k:
                left += 1

            max_len = max(max_len, right - left + 1)

        return max_len

```

#### Step 7.3: Edge Cases Walk & Code Patching

Walk edge cases identified in Step 6:

1. **Empty Array (`tiles = []`)**: Handled correctly (`len(tiles) == 0`, returns `0`).
2. **`k >= total zeros`**: `get_zeros(left, right)` never exceeds `k`, `left` stays `0`, returns `len(tiles)`.
3. **`k == 0`**: Window shrinks whenever `get_zeros(left, right) > 0`, correctly measures max streak of existing `1`s.
4. **Out of bounds update / invalid tile**: Add safety validation guards in `update()`.

```python
class DynamicFootpath:
    def __init__(self, tiles: list[int]):
        self.tiles = list(tiles)
        self.bit = FenwickTree(len(tiles))
        for i, val in enumerate(self.tiles):
            if val == 0:
                self.bit.add(i, 1)

    def update(self, index: int, value: int) -> None:
        # Edge Case Patch: Validate input bounds and values
        if not (0 <= index < len(self.tiles)) or value not in (0, 1):
            return

        if self.tiles[index] == value:
            return

        delta = 1 if value == 0 else -1
        self.bit.add(index, delta)
        self.tiles[index] = value

    def query(self, k: int) -> int:
        if not self.tiles:
            return 0

        def get_zeros(left: int, right: int) -> int:
            if left > right:
                return 0
            left_sum = self.bit.query(left - 1) if left > 0 else 0
            return self.bit.query(right) - left_sum

        left = 0
        max_len = 0

        for right in range(len(self.tiles)):
            while get_zeros(left, right) > k:
                left += 1

            max_len = max(max_len, right - left + 1)

        return max_len

```

---

### 8. Complexity & Optimization Commentary

* **`update(index, value)`**:
* **Time:** $\mathcal{O}(\log N)$ for Fenwick Tree point update.
* **Space:** $\mathcal{O}(1)$ auxiliary.


* **`query(k)`**:
* **Time:** $\mathcal{O}(N \log N)$. Right pointer moves $N$ times. Left pointer moves at most $N$ times. Each `get_zeros` range query takes $\mathcal{O}(\log N)$ time.
* **Space:** $\mathcal{O}(N)$ total space for storing `tiles` and `FenwickTree`.



#### Optional Query Optimization ($\mathcal{O}(N \log N) \rightarrow \mathcal{O}(N)$ via Binary Lifting)

Instead of range querying BIT at each step, binary lifting directly on the Fenwick Tree yields the index of the $K$-th zero in $\mathcal{O}(\log N)$ time, reducing `query(k)` to $\mathcal{O}(N)$ total. However, the two-pointer range query solution remains preferred during interview coding due to readability and ease of verification.