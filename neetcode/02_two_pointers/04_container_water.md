### question
You are given an integer array `heights` where `heights[i]` represents the height of the ithith bar.
You may choose any two bars to form a container. Return the maximum amount of water a container can store.

### 1. Restate

Given array of heights. Pick two vertical lines. Form a container. Maximize trapped water (area).
Area = width $\times$ height.
Width = distance between indices.
Height = shorter line of the two chosen.

### 2. Clarify

* Inputs: Integer array `heights`.
* Constraints: $2 \le n \le 10^5$.
* Values: Non-negative integers.
* Output: Integer representing maximum area.
* Confirm: Lines cannot be slanted. Area is strictly rectangular.

### 3. Hand-Trace

Input: `[1, 8, 6, 2, 5, 4, 8, 3, 7]`
Indices: `0` to `8`.
Try edges: Index `0` (height `1`) and `8` (height `7`).
Width = `8 - 0 = 8`.
Height = $\min(1, 7) = 1$.
Area = $8 \times 1 = 8$.

Shrink width to find taller lines: Move index `0` to `1` (height `8`).
Try: Index `1` (height `8`) and `8` (height `7`).
Width = `8 - 1 = 7`.
Height = $\min(8, 7) = 7$.
Area = $7 \times 7 = 49$.

### 4. Brainstorm & Complexity

* **Idea A (Brute Force):** Nested loops. Test every pair $(i, j)$.
Complexity: Time $O(n^2)$, Space $O(1)$. Fails scale ($n = 10^5$).
* **Idea B (Two Pointers):** Start widest. Width decreases every step. To increase area, must increase bottleneck height. Move the pointer pointing to the shorter line inward.
Complexity: Time $O(n)$, Space $O(1)$.

### 5. Suggest Solutions

1. **Brute Force:** Hand-trace all combinations. Simple, highly readable, but times out.
2. **Two Pointers:** Start wide, aggressively hunt taller lines by abandoning the shorter boundary. Simple logic, optimal time. Prefer this.

### 6. Outline

```python
def maxArea(heights: list[int]) -> int:
    """
    Reframe: Start widest. Move shorter boundary inward to hunt for greater height.
    State: left and right pointers, chosen because we evaluate outer boundaries moving inwards.
    Invariant: Container width strictly decreases. Shorter side is always abandoned.

    calc_area(left, right) = computes width * min height at pointers.

    Core logic:
    - place pointers at array ends
    - while left hasn't met right:
        - compute area using calc_area
        - update global max area
        - if left height is shorter, move left pointer right
        - otherwise, move right pointer left
    Edge cases:
    - heights are equal: moving either is fine (defaults to moving right).
    - exactly two elements: loop runs once, correctly returns base area.
    """

```

### 7. Iterative Implementation

**Skeleton:**

```python
def maxArea(heights: list[int]) -> int:
    # init left, right
    # init max_val
    # while left < right:
    #   area = calc_area(left, right)
    #   update max_val
    #   move shorter pointer
    # return max_val

```

**Iteration 1: Core Logic (using helper)**

```python
def maxArea(heights: list[int]) -> int:
    left = 0
    right = len(heights) - 1 # Note: placed at array ends
    max_val = 0

    while left < right:
        # Note: evaluate current state
        area = calc_area(heights, left, right)
        max_val = max(max_val, area)

        # Note: abandon shorter line
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1

    return max_val

def calc_area(heights, l, r):
    return min(heights[l], heights[r]) * (r - l)

```

**Check Edge Cases:**

* *Equal heights:* `heights[left] == heights[right]` hits the `else` block, `right -= 1`. Valid, since width decreases, area can't increase unless both inner lines are taller.
* *Size 2 array:* Works perfectly without out-of-bounds errors.
* No patches needed. Core logic holds.

### 8. Complexity & Optimizations

* **Time:** $O(n)$. Each array element visited once.
* **Space:** $O(1)$. Only storing integer variables.
* **Optimization:** Python function calls inside `while` loops introduce high overhead. Inline `calc_area` to remove stack pushes. Readability remains high.

**Final Code:**

```python
def maxArea(heights: list[int]) -> int:
    left = 0
    right = len(heights) - 1
    max_val = 0

    while left < right:
        # Inlined calc_area for constant-time performance boost
        current_height = min(heights[left], heights[right])
        width = right - left
        max_val = max(max_val, current_height * width)

        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1

    return max_val

```