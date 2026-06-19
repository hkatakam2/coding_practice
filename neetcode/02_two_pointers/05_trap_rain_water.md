### question
You are given an array of non-negative integers `height` which represent an elevation map. Each value `height[i]` represents the height of a bar, which has a width of `1`.
Return the maximum area of water that can be trapped between the bars.

**1. Restating**
Given 2D elevation map. Bars have width 1. Goal: calculate total trapped rain water volume between bars after raining.

**2. Clarifying Questions & I/O**

* **Input:** List of non-negative integers (e.g., `[0,1,0,2,1,0,1,3,2,1,2,1]`).
* **Output:** Integer representing total volume (e.g., `6`).
* **Questions:** Can map be empty? (Yes -> return 0). Negative heights? (No, prompt says non-negative).

**3. Example By Hand**
Input: `[0, 1, 0, 2, 1, 0, 1, 3]`
Water above any bar = `min(highest_bar_left, highest_bar_right) - current_height`. (If negative, 0).

* Bar 0 (0): edge, traps 0.
* Bar 1 (1): edge-bound, traps 0.
* Bar 2 (0): max left=1, max right=3. min(1,3) - 0 = 1.
* Bar 3 (2): max left=1, max right=3. min(1,3) - 2 < 0 -> 0.
* Bar 4 (1): max left=2, max right=3. min(2,3) - 1 = 1.
* Bar 5 (0): max left=2, max right=3. min(2,3) - 0 = 2.
* Bar 6 (1): max left=2, max right=3. min(2,3) - 1 = 1.
* Bar 7 (3): edge, traps 0.
Total = 1 + 0 + 1 + 2 + 1 = 5.

**4. Brainstorming**

* **A. Brute Force (By Hand method):** For each bar, scan left to find max, scan right to find max. Calculate trapped water.
* *Complexity:* O(N^2) Time, O(1) Space.


* **B. Precomputed Boundaries (Dynamic Programming):** Do one pass left-to-right to save max lefts. Do one pass right-to-left to save max rights. Final pass calculates water.
* *Complexity:* O(N) Time, O(N) Space.


* **C. Two Pointers:** Pointers at both ends. Move the smaller one inwards, tracking maxes along the way.
* *Complexity:* O(N) Time, O(1) Space.



**5. Suggest Solutions**
Prefer clear, straightforward approaches.

1. **Approach A (Brute Force):** Direct translation of by-hand step. Too slow for large inputs, but logically sound.
2. **Approach B (Precomputed Boundaries):** Best balance of simplicity and efficiency. It strictly mimics the by-hand logic but caches the redundant left/right scans. We will implement this.

**6. Outline**

```python
def trap(height):
    """
    Reframe: Water trapped above a bar is dictated by the shortest of the tallest bars to its immediate left and right.
    State: two lists recording tallest bar seen so far from left and from right, chosen because caching avoids recomputing maxes repeatedly.
    Invariant: left cache holds maximum height from start up to current point; right cache holds maximum from end down to current point.

    tallestLeft(point) = highest bar from start to this point
    tallestRight(point) = highest bar from end to this point
    waterAbove(point) = shortest of the two tallest boundaries minus bar's height

    Core logic:
    - gather tallest boundaries for all points from the left
    - gather tallest boundaries for all points from the right
    - for every point, calculate water trapped using boundaries
    - accumulate total water
    - return total

    Edge cases:
    - map with fewer than 3 bars (impossible to trap water)
    """

```

**7. Iterative Implementation**

*Iteration 1: Skeleton with helper stubs.*

```python
def trap(height):
    # TODO: implement left scan
    left_boundaries = get_left_boundaries(height)
    
    # TODO: implement right scan
    right_boundaries = get_right_boundaries(height)
    
    total_water = 0
    # TODO: calculate water at each point
    
    return total_water

```

*Iteration 2: Implement boundary helpers (Happy Path).*

```python
def trap(height):
    # Added left scan logic: carry forward the maximum seen
    left_boundaries = []
    current_max = 0
    for h in height:
        current_max = max(current_max, h)
        left_boundaries.append(current_max)
    
    # Added right scan logic: carry backward the maximum seen
    right_boundaries = [0] * len(height)
    current_max = 0
    for i in reversed(range(len(height))):
        current_max = max(current_max, height[i])
        right_boundaries[i] = current_max
    
    total_water = 0
    # TODO: calculate water at each point
    
    return total_water

```

*Iteration 3: Implement core water calculation (Happy Path Complete).*

```python
def trap(height):
    left_boundaries = []
    current_max = 0
    for h in height:
        current_max = max(current_max, h)
        left_boundaries.append(current_max)
    
    right_boundaries = [0] * len(height)
    current_max = 0
    for i in reversed(range(len(height))):
        current_max = max(current_max, height[i])
        right_boundaries[i] = current_max
    
    total_water = 0
    # Added core water logic: min(left, right) - height
    for i in range(len(height)):
        bounded_height = min(left_boundaries[i], right_boundaries[i])
        total_water += bounded_height - height[i]
        
    return total_water

```

*Iteration 4: Patch Edge Cases.*
Walk the edge cases from Step 6. Map with fewer than 3 bars cannot trap water. The code currently handles this without crashing (loops just don't execute or compute 0), but an early exit is cleaner and safer.

```python
def trap(height):
    # PATCH: Edge case - less than 3 bars
    if len(height) < 3:
        return 0

    left_boundaries = []
    current_max = 0
    for h in height:
        current_max = max(current_max, h)
        left_boundaries.append(current_max)
    
    right_boundaries = [0] * len(height)
    current_max = 0
    for i in reversed(range(len(height))):
        current_max = max(current_max, height[i])
        right_boundaries[i] = current_max
    
    total_water = 0
    for i in range(len(height)):
        bounded_height = min(left_boundaries[i], right_boundaries[i])
        total_water += bounded_height - height[i]
        
    return total_water

```

**8. Complexity & Optimization**

* **Current Complexity:** O(N) Time, O(N) Space.
* **Expensive Sections:** We iterate the array 3 times and store 2 extra arrays. Space is O(N).
* **Optimization (Approach C):** We only ever care about `min(left_max, right_max)`. If we keep a `left` pointer and `right` pointer, the smaller of `left_max` and `right_max` dictates the water level for the corresponding pointer.
* *Optimized Code (Two Pointers - O(1) Space):*

```python
def trap_optimized(height):
    if len(height) < 3: return 0
    
    left, right = 0, len(height) - 1
    left_max, right_max = 0, 0
    total_water = 0
    
    while left < right:
        if height[left] < height[right]:
            # Left side is the bottleneck
            if height[left] >= left_max:
                left_max = height[left]
            else:
                total_water += left_max - height[left]
            left += 1
        else:
            # Right side is the bottleneck
            if height[right] >= right_max:
                right_max = height[right]
            else:
                total_water += right_max - height[right]
            right -= 1
            
    return total_water

```