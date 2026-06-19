### question
Given an array of integers `numbers` that is sorted in non-decreasing order.
Return the indices (1-indexed) of two numbers, `[index1, index2]`, such that they add up to a given target number `target` and `index1 < index2`. Note that `index1` and `index2` cannot be equal, therefore you may not use the same element twice.
There will always be exactly one valid solution.
Your solution must use O(1)O(1) additional space.

### 1. Restate

Given sorted array `numbers` and `target`. Find two distinct elements summing to `target`. Return their 1-based indices `[index1, index2]`. $O(1)$ space constraint. Guaranteed exactly one valid solution.

### 2. Clarifying & Confirming

* Inputs: Sorted integer array (can have negatives, duplicates). Target integer.
* Outputs: Array of two integers (1-indexed).
* Example: `numbers = [2, 7, 11, 15]`, `target = 9` -> `[1, 2]`.
* Constraints check: No hash map allowed due to $O(1)$ space rule.

### 3. Hand-Trace Example

Input: `numbers = [2, 7, 11, 15]`, `target = 9`.

1. Look at edges: `2` and `15`. Sum = 17.
2. 17 > 9. Too large. Need smaller sum. Since sorted, shift right edge leftwards.
3. Look at `2` and `11`. Sum = 13.
4. 13 > 9. Shift right edge leftwards again.
5. Look at `2` and `7`. Sum = 9. Match.
6. Indices: 0, 1. Convert to 1-based: 1, 2. Output: `[1, 2]`.

### 4. Brainstorming & Complexity

* **Brute force:** Nested loops. $O(N^2)$ time, $O(1)$ space. Slow.
* **Hash Map:** Store seen numbers. $O(N)$ time, $O(N)$ space. Violates space constraint.
* **Binary Search:** Iterate each element, binary search for complement in remaining array. $O(N \log N)$ time, $O(1)$ space. Good.
* **Two Pointers (Hand-Trace Method):** Start at ends. Move left pointer right to increase sum, right pointer left to decrease. $O(N)$ time, $O(1)$ space. Optimal.

### 5. Suggest Solutions

Prefer Two Pointers. Simplest, matches hand-trace, cleanly exploits sorted property without complex indexing (unlike Binary Search), meets strict $O(1)$ space constraint natively.

### 6. Outline

```python
def two_sum(numbers: list[int], target: int) -> list[int]: 
     """
    Reframe: Shrink search space from both ends exploiting sorted order.
    State: left pointer, right pointer, chosen because shrinking window from bounds safely discards invalid pairs.
    Invariant: The target pair always lies within the inclusive range [left, right].

    current_sum(left, right) = calculates sum of values at left and right pointers.
    format_output(left, right) = formats zero-based indices into 1-based output array.

    Core logic:
    - loop while left pointer is strictly less than right pointer
    - calculate current sum
    - if current sum equals target, return formatted output
    - if current sum is too small, increment left pointer
    - if current sum is too large, decrement right pointer
    
    Edge cases:
    - No edge cases disrupt happy path. Problem guarantees exactly one solution; loop will never terminate without returning.
     """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton with helpers**

```python
def two_sum(numbers: list[int], target: int) -> list[int]:
    # TODO: init pointers
    
    # loop until pointers cross
    while left < right:
        # get sum
        # check sum vs target
        # adjust pointers
        pass

```

**Iteration 2: Adding Core Logic Chunks**

```python
def two_sum(numbers: list[int], target: int) -> list[int]:
    left = 0 # NEW: init start
    right = len(numbers) - 1 # NEW: init end
    
    while left < right:
        curr = current_sum(left, right) # NEW: get sum helper
        
        if curr == target: # NEW: match condition
            return format_output(left, right)
        elif curr < target: # NEW: need larger sum
            left += 1
        else: # NEW: need smaller sum
            right -= 1

```

**Iteration 3: Full Core Logic (inlining dummy helpers)**

```python
def two_sum(numbers: list[int], target: int) -> list[int]:
    left = 0 
    right = len(numbers) - 1 
    
    while left < right:
        curr = numbers[left] + numbers[right] # CHANGED: inlined sum logic
        
        if curr == target: 
            return [left + 1, right + 1] # CHANGED: inlined 1-based index formatting
        elif curr < target: 
            left += 1
        else: 
            right -= 1

```

**Edge Cases:**
Reviewing edge cases from Step 6: None. Problem guarantees exactly one solution. Array minimum length is 2. Elements fit in standard memory. Left will always be less than right when the solution is hit. Code needs no patches.

### 8. Complexity & Optimizations

* **Time Complexity:** $O(N)$. At worst, left and right pointers meet in the middle, inspecting each element at most once.
* **Space Complexity:** $O(1)$. Only storing two integer pointers (`left`, `right`) and one integer sum (`curr`).
* **Optimizations:** Code is already optimally simple. No expensive operations. Array lookups are $O(1)$. No algorithmic optimizations necessary or possible given limits.