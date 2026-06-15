### question
Given an array of integers `nums` and an integer `target`, return the indices `i` and `j` such that `nums[i] + nums[j] == target` and `i != j`.
You may assume that every input has exactly one pair of indices `i` and `j` that satisfy the condition.
Return the answer with the smaller index first.

### 1. Restate

Array `nums`, int `target`. Find indices `i`, `j` where `nums[i] + nums[j] == target`. Condition: `i != j`. Return `[smaller_index, larger_index]`. Exactly one valid pair exists.

### 2. Clarify

* Negatives allowed? Yes.
* Array sorted? No.
* Duplicates allowed? Yes.
* Memory limits? Standard.

### 3. Hand-Trace

Input: `nums = [3, 2, 4]`, `target = 6`

* Current `3` (idx 0). Need `3`. Not seen yet. Store `3` at idx 0.
* Current `2` (idx 1). Need `4`. Not seen yet. Store `2` at idx 1.
* Current `4` (idx 2). Need `2`. Seen `2` at idx 1.
* Return `[1, 2]`.

### 4. Brainstorm & Complexity

1. **Brute Force:** Nested loops. Check all pairs. Time O(N^2), Space O(1). Slow.
2. **Sort + Two Pointers:** Sort array. Left/right pointers. Track original indices. Time O(N log N), Space O(N). Complex tracking.
3. **Hash Map (1-pass):** Track seen numbers and indices. Check for complement. Time O(N), Space O(N). Fast, clean. (Matches Step 3 hand-trace).

### 5. Suggest Solution

Select Hash Map (1-pass). Simple, linear time, straightforward logic. Explaining state over time is highly readable.

### 6. Outline Core Logic

```python
def twoSum(nums, target):  # -> list[int]
    """
    Reframe: Find missing complement for each number as we scan.
    State: Hash map (seen_val_to_idx), chosen because O(1) lookups find complements instantly.
    Invariant: Map only contains elements processed *before* current element, preventing self-matching.

    Core logic:
    - for each item in sequence:
        - calculate required complement to hit target
        - if complement exists in our seen record:
            - return recorded index of complement and current index
        - otherwise:
            - record current item and its index in seen record
            
    Edge cases:
    - Same value used twice to hit target (e.g., [3, 3], target 6). 
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton & Plain English Stubs**

```python
def twoSum(nums, target):
    # setup state
    
    # iterate items
        # get complement
        
        # check if complement seen
            # return pair
            
        # mark seen
        
    return []

```

**Iteration 2: Translating stubs to logic (Happy Path)**

```python
def twoSum(nums, target):
    # setup state
    seen = {} # value -> index
    
    # iterate items
    for index, num in enumerate(nums): # ADDED: loop over nums
        # get complement
        complement = target - num # ADDED: target math
        
        # check if complement seen
        if complement in seen: # ADDED: map lookup
            # return pair
            return [seen[complement], index] # ADDED: return ordered indices
            
        # mark seen
        seen[num] = index # ADDED: store current
        
    return []

```

**Iteration 3: Walking Edge Cases**
*Edge Case:* Same value used twice to hit target (e.g., `nums = [3, 3]`, `target = 6`).
*Walkthrough on current code:*

1. `num = 3` (idx 0). `complement = 3`. Not in `seen`. `seen[3] = 0`.
2. `num = 3` (idx 1). `complement = 3`. Is in `seen`. Returns `[seen[3], 1]` -> `[0, 1]`.
*Result:* Handled perfectly. Invariant holds because we check map *before* adding current element, preventing index from matching itself.
*Note:* No code patch needed. Core logic naturally covers edge cases based on problem constraints (exactly one solution guaranteed).

### 8. Complexity & Optimizations

* **Time Complexity:** O(N). Single pass through array. Hash map lookups average O(1).
* **Space Complexity:** O(N). Worst case, store N-1 elements in hash map before finding match.
* **Optimizations:** Solution is already mathematically optimal for time. No further algorithmic optimizations apply without sacrificing space constraints, which isn't required here. Code is pythonic and maximally readable.