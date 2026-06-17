## question
You are given an array of integers `nums`, where `nums[i]` represents the maximum length of a jump towards the right from index `i`. For example, if you are at `nums[i]`, you can jump to any index `i + j` where:

* `j <= nums[i]`
* `i + j < nums.length`
You are initially positioned at `nums[0]`.
Return the minimum number of jumps to reach the last position in the array (index `nums.length - 1`). You may assume there is always a valid answer.

**1. Restate**
Given array of max jump lengths. Start at index 0. Find fewest jumps to reach last index.

**2. Clarify**

* Inputs: `nums`, array of integers >= 0.
* Outputs: Integer, min jumps.
* Constraints: Always a valid path? Yes. Length >= 1? Yes.

**3. Example by Hand**
`nums = [2, 3, 1, 1, 4]`

* Start idx 0 (val 2). Options: idx 1, idx 2.
* Path A: idx 0 -> idx 1 (val 3) -> can reach idx 2, 3, 4. (2 jumps total).
* Path B: idx 0 -> idx 2 (val 1) -> can reach idx 3 (val 1) -> can reach idx 4. (3 jumps total).
* Min jumps = 2.

**4. Brainstorm & Complexity**

* **Option A (DP):** `dp[i]` = min jumps from `i` to end. Check all reachable indices from `i`, take min + 1. Time: O(N^2), Space: O(N).
* **Option B (BFS / Level Order):** Treat reachable ranges as levels. Level 0: idx 0. Level 1: idx 1 to 2. Level 2: furthest reach from Level 1. Time: O(N), Space: O(1).

**5. Suggest Solutions**
Prefer Option B (Level Order/Greedy). It mimics the human hand-trace: "In jump 1, I can reach up to index 2. Let me check all indices up to 2 to see the furthest I can go for jump 2." Simple, straight forward, avoids nested loops of DP.

**6. Outline**

```python
def jump(nums): 
    """
    Reframe: Process array in contiguous blocks (levels), where each block represents one jump.
    State: `current_jump_end` (end of current block), `furthest_reach` (max reach seen so far). chosen because it bounds the BFS level implicitly without extra arrays.
    Invariant: At index i, `jumps` reflects minimum steps to reach `current_jump_end`.

    update_furthest(current_furthest, index) = returns max of current furthest or (index + jump length).
    
    Core logic:
    - Iterate through array up to the second-to-last element
    - Continually calculate the furthest reachable index from the current position
    - If we reach the end of our current jump block:
        - Increment jump count
        - Start a new jump block ending at the furthest reachable index we just found
    
    Edge cases:
    - Array length is 1 (start is already the end, 0 jumps)
    """

```

**7. Iterative Implementation**

**Iteration 1: Skeleton with stubs**

```python
def jump(nums):
    jumps = 0
    current_jump_end = 0
    furthest_reach = 0
    
    # Core logic outline
    for i in range(len(nums) - 1): # stop before last element
        # keep track of furthest we can go
        furthest_reach = get_furthest(furthest_reach, i, nums[i])
        
        # if we hit the limit of current jump
        if i == current_jump_end:
            jumps += 1
            current_jump_end = furthest_reach
            
    return jumps

def get_furthest(current_furthest, index, jump_length):
    # stub: return max reach
    pass

```

**Iteration 2: Inline helpers & refine logic**

```python
def jump(nums):
    jumps = 0
    current_jump_end = 0
    furthest_reach = 0
    
    for i in range(len(nums) - 1): 
        # inline helper: furthest reach from this index is index + max jump
        # updated: track absolute furthest seen so far
        furthest_reach = max(furthest_reach, i + nums[i])
        
        if i == current_jump_end:
            jumps += 1
            current_jump_end = furthest_reach
            
    return jumps

```

**Iteration 3: Patch Edge Cases**
Core logic is complete. Review edge cases from Step 6.

* *Array length 1:* `nums = [0]`. `len(nums) - 1` is `0`. Loop `for i in range(0)` skips execution. Returns `jumps = 0`. Happy path already handles this perfectly. No patching needed.

Final Code:

```python
def jump(nums):
    jumps = 0
    current_jump_end = 0
    furthest_reach = 0
    
    # Stop before last element because reaching it doesn't require jumping again
    for i in range(len(nums) - 1): 
        furthest_reach = max(furthest_reach, i + nums[i])
        
        # Reached the boundary of the current jump level
        if i == current_jump_end:
            jumps += 1
            current_jump_end = furthest_reach
            
    return jumps

```

**8. Complexity & Optimizations**

* **Time Complexity:** O(N). Single pass through the array. `max()` is O(1).
* **Space Complexity:** O(1). Only three integer variables stored.
* **Optimizations:** Algorithm is optimally bounded. Cannot solve without inspecting elements (O(N) minimum). An early exit could be added: `if current_jump_end >= len(nums) - 1: break` inside the `if` block to halt the loop early if we already can reach the end, saving a few iterations, but worst-case remains O(N). Simple logic preferred over minor early exit here.