### question
Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

 

Example 1:


Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
Explanation: The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.
Example 2:

Input: height = [4,2,0,3,2,5]
Output: 9


**1. Restating the Question**
Given an array of non-negative integers representing bar elevations of width 1, calculate the total units of water trapped between the bars after raining.

**2. Clarifying Questions & Constraints**

* **Empty / Short input:** Can `height` have fewer than 3 bars? (Yes; cannot trap water if length $< 3$, return `0`).
* **Values:** Can heights be negative? (No, non-negative integers only).
* **Bounds:** What is the max array length? (Typically $N \le 10^5$; heights fit in standard integer).
* **Return type:** Single integer representing total trapped water units.

**3. Manual Walkthrough**
Input: `height = [4, 2, 0, 3, 2, 5]`
For any bar $i$, trapped water is determined by: $\text{water}[i] = \max(0, \min(\text{max\_left}[i], \text{max\_right}[i]) - \text{height}[i])$.

| Index $i$ | Height | Max Left | Max Right | Min(L, R) | Water at $i$ |
| --- | --- | --- | --- | --- | --- |
| **0** | 4 | 4 | 5 | 4 | $4 - 4 = 0$ |
| **1** | 2 | 4 | 5 | 4 | $4 - 2 = 2$ |
| **2** | 0 | 4 | 5 | 4 | $4 - 0 = 4$ |
| **3** | 3 | 4 | 5 | 4 | $4 - 3 = 1$ |
| **4** | 2 | 4 | 5 | 4 | $4 - 2 = 2$ |
| **5** | 5 | 5 | 5 | 5 | $5 - 5 = 0$ |

Total water = $0 + 2 + 4 + 1 + 2 + 0 = 9$.

---

**4. Brainstorming & Complexity**

* **Approach 1: Brute Force**
* For each index $i$, scan left for maximum height, scan right for maximum height.
* Time: $O(N^2)$, Space: $O(1)$.


* **Approach 2: Precomputed Prefix & Suffix Maximums (Selected)**
* Precompute `left_max` and `right_max` arrays in linear passes. Calculate water in one final pass.
* Time: $O(N)$, Space: $O(N)$.
* *Trade-off:* Clear, robust, direct mirror of the manual calculation.


* **Approach 3: Two Pointers**
* Maintain `left_max` and `right_max` dynamically using inward-moving pointers.
* Time: $O(N)$, Space: $O(1)$.



---

**5. Selected Solution**
Use **Precomputed Prefix/Suffix Maximums (Approach 2)**. It avoids pointer edge cases, matches manual reasoning 1-to-1, and is trivial to verify.

---

**6. Implementation Outline & Docstring**

```python
def trap(height: list[int]) -> int:
    """
    Reframe: Water trapped above any bar is bounded strictly by the shorter
             of the tallest bars to its left and right.
    State: left_maxes and right_maxes arrays, chosen because random access
           to boundary ceilings enables an O(1) calculation per bar.
    Invariant: At every bar, trapped water is non-negative and depends solely
               on the global left and right bounds relative to that bar.

    get_left_maxes(height) = array where each index holds the max height from 0 to i.
    get_right_maxes(height) = array where each index holds the max height from i to n-1.
    water_at_bar(bar, left_cap, right_cap) = min(left_cap, right_cap) - bar.

    Core logic:
    - Precompute left boundary ceilings across all bars.
    - Precompute right boundary ceilings across all bars.
    - Iterate through each bar, compute trapped water using its precomputed boundaries,
      and sum the results.

    Edge cases:
    - Array length < 3: impossible to trap water (requires at least two walls and a middle valley).
    - Monotonically increasing / decreasing heights: bounds equal the bar itself, trapped water is 0.
    - Flat terrain (all same height): trapped water is 0.
    """
    pass

```

---

**7. Iterative Implementation**

**Iteration 1: Skeleton with stubs**

```python
def trap(height: list[int]) -> int:
    # Stub helper functions for core logical steps
    def get_left_maxes(arr):
        pass  # TODO: compute prefix maxes

    def get_right_maxes(arr):
        pass  # TODO: compute suffix maxes

    left_maxes = get_left_maxes(height)
    right_maxes = get_right_maxes(height)

    total_water = 0
    for i in range(len(height)):
        water_level = min(left_maxes[i], right_maxes[i])
        total_water += water_level - height[i]

    return total_water

```

**Iteration 2: Implement helper logic**

```python
def trap(height: list[int]) -> int:
    n = len(height)

    # Compute prefix maxes (left to right)
    left_maxes = [0] * n
    current_max = 0
    for i in range(n):
        current_max = max(current_max, height[i])
        left_maxes[i] = current_max

    # Compute suffix maxes (right to left)
    right_maxes = [0] * n
    current_max = 0
    for i in range(n - 1, -1, -1):
        current_max = max(current_max, height[i])
        right_maxes[i] = current_max

    # Accumulate water per bar
    total_water = 0
    for i in range(n):
        total_water += min(left_maxes[i], right_maxes[i]) - height[i]

    return total_water

```

**Iteration 3: Walking edge cases and adding guard clause**

* *Edge 1:* `len(height) < 3`: Loop runs safely, but early return avoids allocation.
* *Edge 2:* All elements identical / monotonic: `min(left_maxes[i], right_maxes[i]) == height[i]`, adds `0` each step. Safe.

```python
def trap(height: list[int]) -> int:
    # Edge case: need at least 3 bars to form a basin
    if not height or len(height) < 3:
        return 0

    n = len(height)

    # 1. Build prefix max array
    left_max = [0] * n
    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], height[i])

    # 2. Build suffix max array
    right_max = [0] * n
    right_max[-1] = height[-1]
    for i in range(n - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], height[i])

    # 3. Sum trapped water
    total_water = 0
    for i in range(n):
        total_water += min(left_max[i], right_max[i]) - height[i]

    return total_water

```

---

**8. Complexity & Space Optimization**

* **Prefix/Suffix Solution Complexity:**
* **Time:** $O(N)$ — three linear passes.
* **Space:** $O(N)$ — two arrays of size $N$.


* **Space Optimization to $O(1)$ (Two Pointers):**
Because water height is strictly limited by $\min(\text{left\_max}, \text{right\_max})$, we don't need the entire array if we process from the side with the smaller current boundary.

```python
def trap_optimized(height: list[int]) -> int:
    if not height or len(height) < 3:
        return 0

    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    total_water = 0

    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            total_water += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            total_water += right_max - height[right]

    return total_water

```

* **Optimized Complexity:**
* **Time:** $O(N)$ — single pass.
* **Space:** $O(1)$ — constant auxiliary space.