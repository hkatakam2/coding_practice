## question
Given an integer array nums, return the length of the longest strictly increasing subsequence.
A subsequence is a sequence that can be derived from the given sequence by deleting some or no elements without changing the relative order of the remaining characters.

For example, "cat" is a subsequence of "crabt".

### 1. Restating the Question

Find maximum count of elements from array that maintain original order and strictly increase in value.

### 2. Clarifying Questions, Inputs, Outputs

* **Input:** `nums`, array of integers.
* **Output:** Integer, length of longest strictly increasing subsequence (LIS).
* **Clarifications:** * Empty array possible? (Assume yes, return 0).
* Negative numbers? (Yes, handled normally).
* Strictly increasing? (Yes, duplicates like `[2, 2]` don't count).



### 3. Manual Walkthrough

Input: `[10, 9, 2, 5, 3, 7, 101, 18]`

* Start left to right. Track best subsequences.
* `10`: `[10]`. Length 1.
* `9`: `[9]`. Length 1.
* `2`: `[2]`. Length 1.
* `5`: Append to `2` -> `[2, 5]`. Length 2.
* `3`: Append to `2` -> `[2, 3]`. Length 2.
* `7`: Append to `[2, 5]` or `[2, 3]` -> `[2, 3, 7]`. Length 3.
* `101`: Append to `[2, 3, 7]` -> `[2, 3, 7, 101]`. Length 4.
* `18`: Append to `[2, 3, 7]` -> `[2, 3, 7, 18]`. Length 4.
* Max length across all built sequences: 4.

### 4. Brainstorming & Complexity

* **Brute Force:** Generate all $2^n$ subsequences. Check if increasing. Time: $O(2^n)$. Space: $O(n)$. Too slow.
* **Recursion + Memoization (Top-Down DP):** For each element, include or exclude. Memoize `(currentIndex, prevIndex)`. Time: $O(n^2)$. Space: $O(n^2)$. Better, but recursion overhead.
* **Iterative DP (Bottom-Up):** Like manual walkthrough. Store max LIS ending at each index. For current index, look at all previous. If previous is smaller, current LIS = max(current, previous + 1). Time: $O(n^2)$. Space: $O(n)$.
* **Binary Search (Patience Sort):** Maintain active sequence of smallest tail elements. Binary search to update. Time: $O(n \log n)$. Space: $O(n)$.

### 5. Suggested Solution

Always prefer simple and clear. **Iterative Bottom-Up DP** mirrors the manual approach directly. It is highly intuitive to explain: "To know the longest sequence ending *here*, look at all valid sequences ending *before here* and add 1."

### 6. Outline Implementation

```python
def lengthOfLIS(nums): 
    """
    Reframe: Longest path in a DAG where edges are strictly increasing values.
    State: Array maintaining max LIS length ending exactly at each element, chosen because optimal substructure applies (best result at current step relies on best results of previous valid steps).
    Invariant: For any evaluated element, its stored LIS length is the absolute maximum possible using strictly smaller elements before it.

    get_max_previous_chain(current_val, previous_elements, recorded_lengths) = scans previous elements, filters for those smaller than current_val, and returns the maximum length among them.

    Core logic:
    - Create a record of sequence lengths for each element, all starting at 1 (representing a sequence of just that element).
    - For each element in the array:
        - Find the longest strictly increasing sequence ending before this element that we can legally append to, using get_max_previous_chain.
        - Update current element's recorded length to be that max previous sequence + 1.
    - Return the highest number found in the entire record of lengths.

    Edge cases:
    - Empty input array (return 0).
    - Array with 1 element (loop doesn't trigger, returns 1).
    - All elements identical (no strictly increasing condition met, returns 1).
    - Strictly decreasing array (no valid previous chains, returns 1).
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton with helper stub.**
Translating plain English to structural code.

```python
def lengthOfLIS(nums):
    # Create record of lengths, initially 1
    dp = [1] * len(nums)
    
    # For each element
    for current_idx in range(len(nums)):
        # TODO: Implement get_max_previous_chain logic
        # best_prev = get_max_previous_chain(...)
        # dp[current_idx] = best_prev + 1
        pass
        
    # Return highest number found
    return max(dp) 

```

**Iteration 2: Fleshing out the inner logic (the helper).**
Replacing the stub by looking at all previous elements.

```python
def lengthOfLIS(nums):
    dp = [1] * len(nums)
    
    for current_idx in range(len(nums)):
        # NEW: Implementing get_max_previous_chain directly as a loop
        for prev_idx in range(current_idx):
            # Check if strictly increasing
            if nums[current_idx] > nums[prev_idx]:
                # Update current element's recorded length
                dp[current_idx] = max(dp[current_idx], dp[prev_idx] + 1)
                
    return max(dp)

```

**Iteration 3: Core logic complete. Now addressing Edge Cases.**
Reviewing the docstring edge cases. If `nums` is empty, `max(dp)` throws an error. Needs a patch.

```python
def lengthOfLIS(nums):
    # PATCH: Handle empty array edge case
    if not nums:
        return 0
        
    dp = [1] * len(nums)
    
    for current_idx in range(len(nums)):
        for prev_idx in range(current_idx):
            if nums[current_idx] > nums[prev_idx]:
                dp[current_idx] = max(dp[current_idx], dp[prev_idx] + 1)
                
    return max(dp)

```

### 8. Complexity & Optimization

* **Complexity of current DP solution:** Time is $O(n^2)$ because of the nested loops (checking every previous element for every current element). Space is $O(n)$ for the `dp` array.
* **Expensive Section:** The inner loop `for prev_idx in range(current_idx):`. We are doing a linear scan to find the best previous element.
* **Optimization ($O(n \log n)$):** We don't need to scan everything. We can build an `active_sequence` array.
* If a number is larger than the last item in `active_sequence`, append it (sequence grows).
* If it's smaller, find the *first* number in `active_sequence` that is $\ge$ current number and replace it. (Using binary search). This keeps potential tails as small as possible, allowing longer chains later.



**Optimized Code Implementation:**

```python
import bisect

def lengthOfLIS_optimized(nums):
    if not nums:
        return 0
        
    active_sequence = []
    
    for num in nums:
        # Binary search for the index to replace/insert
        idx = bisect.bisect_left(active_sequence, num)
        
        # If index is at the end, num is largest, append it
        if idx == len(active_sequence):
            active_sequence.append(num)
        # Otherwise, overwrite the first number >= num
        else:
            active_sequence[idx] = num
            
    # The length of active_sequence is the length of LIS
    return len(active_sequence)

```

*Note: `active_sequence` in the optimized version is NOT the actual LIS subsequence elements, but its length is guaranteed to be correct. Time: $O(n \log n)$, Space: $O(n)$.*