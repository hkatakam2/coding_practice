### question
You are given an array of integers heights where heights[i] represents the height of a bar. The width of each bar is 1.

Return the area of the largest rectangle that can be formed among the bars.

### 1. Restating the Question

Given array `heights` representing histogram bars (width 1). Find largest rectangular area completely contained within the bars.

### 2. Clarifying Questions & Confirming I/O

* **Q:** Can `heights` be empty? **A:** Assume yes. Return 0.
* **Q:** Are heights non-negative? **A:** Yes.
* **Q:** Maximum length of `heights`? **A:** Assume large (e.g., 10^5). O(N^2) might time out.
* **Inputs:** `[2, 1, 5, 6, 2, 3]`
* **Outputs:** `10`

### 3. Hand-Tracing Example

Input: `[2, 1, 5, 6, 2, 3]`
Core idea: Every maximal rectangle is bounded by the height of *some* bar. Assume each bar is the shortest bar in our rectangle. Expand left/right until hitting a shorter bar.

* Index 0 (height 2): stops at idx 1 (height 1). Width = 1. Area = 2.
* Index 1 (height 1): expands all the way. Width = 6. Area = 6.
* Index 2 (height 5): stops left at idx 1, right at idx 4. Bounds: [5, 6]. Width = 2. Area = 10.
* Index 3 (height 6): stops left at idx 2, right at idx 4. Bounds: [6]. Width = 1. Area = 6.
* Index 4 (height 2): stops left at idx 1, right at end. Bounds: [5, 6, 2, 3]. Width = 4. Area = 8.
* Index 5 (height 3): stops left at idx 4, right at end. Bounds: [3]. Width = 1. Area = 3.
Max Area = 10.

### 4. Brainstorming Solutions & Complexity

* **Idea 1 (Brute Force Pairs):** Check every pair `(i, j)`, find min height between them, multiply by width. Time: O(N^3). Too slow.
* **Idea 2 (Expand around each bar):** Hand-trace method. For each bar, expand left and right. Time: O(N^2) worst case (sorted array), Space: O(1).
* **Idea 3 (Precompute Boundaries / Monotonic Stack):** Cache the first shorter bar to the left and right using a stack. Time: O(N), Space: O(N).

### 5. Suggest Solutions

Suggest Idea 2 (Expand around each bar) for clarity and ease of explanation. It perfectly maps to human logic (Step 3). Will use this for the base implementation. Idea 3 is a clever optimization to discuss later.

### 6. Outline Implementation

```python
def largestRectangleArea(heights):
    """
    Reframe: Max rectangle must be bounded by the height of at least one bar in the array.
    State: current_max variable, chosen because we only need to track the largest area seen so far.
    Invariant: For any bar treated as the minimum height, we calculate the absolute widest rectangle it can form.

    findLeftBound(current_bar_index) = finds the index of the nearest shorter bar to the left.
    findRightBound(current_bar_index) = finds the index of the nearest shorter bar to the right.
    calcArea(height, left_bound, right_bound) = multiplies height by the distance between bounds.

    Core logic:
    - For each bar in the histogram:
        - Find its left boundary using findLeftBound.
        - Find its right boundary using findRightBound.
        - Calculate rectangle area using calcArea.
        - Update maximum area found so far.
    - Return maximum area.
    
    Edge cases:
    - Empty heights array.
    - Bar expands all the way to the left edge (no shorter bar exists).
    - Bar expands all the way to the right edge (no shorter bar exists).
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton with stubs**

```python
def largestRectangleArea(heights):
    max_area = 0
    
    # stubs
    def findLeftBound(idx): return 0
    def findRightBound(idx): return 0
    def calcArea(h, l, r): return 0

    for i in range(len(heights)):
        left_bound = findLeftBound(i)
        right_bound = findRightBound(i)
        
        area = calcArea(heights[i], left_bound, right_bound)
        max_area = max(max_area, area)
        
    return max_area

```

**Iteration 2: Implementing core logic (Expand around center)**

```python
def largestRectangleArea(heights):
    max_area = 0
    
    # Iterate to expand. Leaving edge cases for next iteration.
    def findLeftBound(idx): 
        curr = idx
        # Keep moving left while taller or equal
        while heights[curr] >= heights[idx]:
            curr -= 1
        return curr

    def findRightBound(idx): 
        curr = idx
        # Keep moving right while taller or equal
        while heights[curr] >= heights[idx]:
            curr += 1
        return curr

    def calcArea(h, left_idx, right_idx): 
        # Width is elements BETWEEN left_idx and right_idx
        width = right_idx - left_idx - 1
        return h * width

    for i in range(len(heights)):
        left = findLeftBound(i)
        right = findRightBound(i)
        
        area = calcArea(heights[i], left, right)
        max_area = max(max_area, area)
        
    return max_area

```

**Iteration 3: Patching Edge Cases**

* *Edge 1:* Empty array -> returns 0 natively? Range is empty, returns 0. Good.
* *Edge 2 & 3:* Out of bounds indexing in `findLeftBound` and `findRightBound`. Need to stop at ends of array.

```python
def largestRectangleArea(heights):
    if not heights: return 0 # Edge 1: Fast fail empty
    
    max_area = 0
    n = len(heights)
    
    def findLeftBound(idx): 
        curr = idx
        # Edge 2: Prevent curr going < 0
        while curr >= 0 and heights[curr] >= heights[idx]:
            curr -= 1
        return curr # Returns -1 if it goes all the way left

    def findRightBound(idx): 
        curr = idx
        # Edge 3: Prevent curr going >= n
        while curr < n and heights[curr] >= heights[idx]:
            curr += 1
        return curr # Returns n if it goes all the way right

    def calcArea(h, left_idx, right_idx): 
        width = right_idx - left_idx - 1
        return h * width

    for i in range(n):
        left = findLeftBound(i)
        right = findRightBound(i)
        area = calcArea(heights[i], left, right)
        max_area = max(max_area, area)
        
    return max_area

```

### 8. Complexity & Optimization

* **Current Complexity:** Time: O(N^2) worst case (e.g., all same heights, expands fully every time). Space: O(1).
* **Commentary:** Expensive section is the repeated expansion. We recalculate boundaries for every bar.
* **Optimization:** Monotonic Stack. We can find all `left_bounds` and `right_bounds` in a single O(N) pass. Stack keeps indices of bars in increasing height order. If we see a shorter bar, we resolve the heights for the taller bars currently in the stack.

**Optimized Implementation (O(N) Time, O(N) Space):**

```python
def largestRectangleArea_optimized(heights):
    max_area = 0
    stack = [] # Stores indices. Heights represented will be strictly increasing.
    
    # Append 0 to flush remaining bars in stack at the end
    heights = heights + [0] 
    
    for i, h in enumerate(heights):
        # Found a shorter bar? Resolve bounded rectangles in stack.
        while stack and heights[stack[-1]] > h:
            height_idx = stack.pop()
            bar_height = heights[height_idx]
            
            # Right bound is current index `i`. 
            # Left bound is the new top of stack after pop.
            left_bound = stack[-1] if stack else -1
            width = i - left_bound - 1
            
            max_area = max(max_area, bar_height * width)
            
        stack.append(i)
        
    return max_area

```