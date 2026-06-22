### question

Leetcode 528. Random Pick with Weight
Given an array of positive weights, implement pickIndex() to return index i with probability w[i]/sum(w)

**1. Restate**
Given array of weights `w`. Return index `i` randomly. Probability of picking `i` must be `w[i] / total_sum`.

**2. Clarify**

* Inputs: `w`, array of positive integers. Size? (Assume 1 to $10^4$).
* Outputs: Integer representing index.
* Constraints: `pickIndex` called many times? (Yes, optimize `pickIndex` over `__init__`).

**3. By-hand Example**
Input: `w = [1, 3, 2]`
Total sum = 6.
Probabilities: index 0 (1/6), index 1 (3/6), index 2 (2/6).
By hand: Expand into flat array matching probabilities.
`expanded = [0, 1, 1, 1, 2, 2]`
Pick random index from 0 to 5.
If random index = 3, `expanded[3]` is `1`. Return `1`.

**4. Brainstorm & Complexity**

* **Approach A (Expanded Array - By Hand):** Expand weights into array of size `total_sum`. Pick random element.
* Time: `__init__` $O(\sum w)$, `pickIndex` $O(1)$.
* Space: $O(\sum w)$. Bad if weights are huge (e.g., `w = [10000000]`). Memory limit exceeded.


* **Approach B (Prefix Sums + Linear Scan):** Map weights to continuous ranges. `[1, 3, 2]` -> ranges `(0,1], (1,4], (4,6]`. Upper bounds = prefix sums: `[1, 4, 6]`. Pick random `R` from 1 to 6. Iterate prefix array to find first bound $\ge R$.
* Time: `__init__` $O(N)$, `pickIndex` $O(N)$.
* Space: $O(N)$.


* **Approach C (Prefix Sums + Binary Search):** Same as B, but use binary search on prefix sums since it's strictly increasing.
* Time: `__init__` $O(N)$, `pickIndex` $O(\log N)$.
* Space: $O(N)$.



**5. Suggest Solutions**
Prefer clear, simple solutions.

1. Approach A (Expanded Array - By Hand method). Simplest conceptually, but fails constraints (Memory).
2. Approach B (Prefix Sum + Linear Scan). Clear, straightforward. Easily fits constraints if $N$ is small.
3. Approach C (Prefix Sum + Binary Search). Optimal.

Select Approach B for core logic outline (simplest), then optimize to Approach C (binary search) in step 8.

**6. Outline**

```python
class Solution:
    def __init__(self, w: list[int]):
        pass

    def pickIndex(self) -> int:
        """
        Reframe: Map weights to continuous buckets. Pick random number, find bucket.
        State: Prefix sums array, chosen because cumulative addition naturally defines upper bounds of buckets.
        Invariant: prefix_sums is sorted strictly ascending.

        generate_random(max_val) = returns random integer from 1 to max_val inclusive.
        find_first_greater_or_equal(target) = scans prefix sums to find first value >= target.

        Core logic:
        - get random target using total sum
        - find first bucket bound greater or equal to target using find_first_greater_or_equal
        - return that bucket's index
        
        Edge cases:
        - array has exactly 1 element
        """
        pass

```

**7. Iterative Implementation**

*Iteration 1: Skeleton with helper stubs.*

```python
import random

class Solution:
    def __init__(self, w: list[int]):
        self.prefix_sums = []
        self.total_sum = 0
        # TODO: build prefix sums

    def pickIndex(self) -> int:
        # TODO: get random target
        # TODO: find and return bucket
        pass

```

*Iteration 2: Implement `__init__` (Core Logic)*

```python
import random

class Solution:
    def __init__(self, w: list[int]):
        # CHANGE: implemented prefix sum building
        self.prefix_sums = []
        current_sum = 0
        for weight in w:
            current_sum += weight
            self.prefix_sums.append(current_sum)
        self.total_sum = current_sum

    def pickIndex(self) -> int:
        # TODO: get random target
        # TODO: find and return bucket
        pass

```

*Iteration 3: Implement `pickIndex` happy path using dummy helper*

```python
import random

class Solution:
    def __init__(self, w: list[int]):
        self.prefix_sums = []
        current_sum = 0
        for weight in w:
            current_sum += weight
            self.prefix_sums.append(current_sum)
        self.total_sum = current_sum

    def pickIndex(self) -> int:
        # CHANGE: core logic realized using dummy helper
        target = random.randint(1, self.total_sum)
        return self._find_first_geq(target)

    def _find_first_geq(self, target: int) -> int:
        # TODO: implement linear scan
        pass

```

*Iteration 4: Implement dummy helper (Linear Scan)*

```python
import random

class Solution:
    def __init__(self, w: list[int]):
        self.prefix_sums = []
        current_sum = 0
        for weight in w:
            current_sum += weight
            self.prefix_sums.append(current_sum)
        self.total_sum = current_sum

    def pickIndex(self) -> int:
        target = random.randint(1, self.total_sum)
        return self._find_first_geq(target)

    def _find_first_geq(self, target: int) -> int:
        # CHANGE: simple linear scan realization
        for i, prefix in enumerate(self.prefix_sums):
            if prefix >= target:
                return i

```

*Patching Edge Cases:*

* `w` has 1 element. E.g., `w = [5]`. `prefix = [5]`. `target` between 1 and 5. Loop runs once, `5 >= target`. Returns `0`. Works perfectly. No patches needed.

**8. Complexity & Optimization**
*Comment on complexity:*
`__init__`: $O(N)$ time, $O(N)$ space.
`pickIndex`: $O(N)$ time due to linear scan in `_find_first_geq`. Since `pickIndex` is called frequently, $O(N)$ is too expensive.
*Optimization:*
`prefix_sums` is strictly increasing (all weights positive). We can replace linear scan with Binary Search. Reduces `pickIndex` time to $O(\log N)$.

*Optimized Code (`_find_first_geq` replacement):*

```python
    def _find_first_geq(self, target: int) -> int:
        # OPTIMIZATION: replace linear scan with binary search
        low, high = 0, len(self.prefix_sums) - 1
        
        while low < high:
            mid = low + (high - low) // 2
            if self.prefix_sums[mid] < target:
                low = mid + 1
            else:
                high = mid
                
        return low

```