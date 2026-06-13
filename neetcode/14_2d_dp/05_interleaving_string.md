## question
You are given an array of integers nums and an integer target.
For each number in the array, you can choose to either add or subtract it to a total sum.

For example, if nums = [1, 2], one possible sum would be "+1-2=-1".
If nums=[1,1], there are two different ways to sum the input numbers to get a sum of 0: "+1-1" and "-1+1".
Return the number of different ways that you can build the expression such that the total sum equals target.

Here is the mock interview simulation for the Target Sum problem.

### 1. Restate

Given integer array `nums` and integer `target`.
Assign `+` or `-` to each element.
Return total count of valid expressions evaluating exactly to `target`.

### 2. Clarify Inputs & Outputs

* **Input:** `nums` (array of integers), `target` (integer).
* **Output:** `int` (number of ways).
* **Clarifications to ask:** Can `nums` contain zeros? (Yes). Are all elements positive? (Usually yes, standard is $0 \le nums[i]$). Can `target` be negative? (Yes). Maximum length of `nums`? (Assume up to ~20, meaning $2^{20}$ is too slow, need optimization).

### 3. Example by Hand

`nums = [1, 2]`, `target = 1`

* Start: sum = 0. Index = 0.
* Item 1 (1):
* Branch A (+1): sum = 1
* Branch B (-1): sum = -1


* Item 2 (2):
* From Branch A: +1 +2 = 3 (Fail), +1 -2 = -1 (Fail)
* From Branch B: -1 +2 = 1 (Match target!), -1 -2 = -3 (Fail)


* Output: 1 way.

### 4. Brainstorming & Complexity

* **Approach 1: Exhaustive Recursion (DFS).** Explore every `+` and `-` path. Matches "by hand" tree logic.
* Time: $O(2^N)$ where N is length of array.
* Space: $O(N)$ for recursion stack.


* **Approach 2: Recursion + Memoization (Top-Down).** Track `(index, current_sum)`. Many paths converge on the same sum at the same index.
* Time: $O(N \times \text{Sum})$.
* Space: $O(N \times \text{Sum})$.


* **Approach 3: Math + Subset Sum (Bottom-Up DP).** Clever optimization. Separate into positive (`P`) and negative (`N`) subsets. `Sum(P) - Sum(N) = target`. Substitute `Sum(N) = Total - Sum(P)`. Result: `Sum(P) = (target + Total) / 2`. Reduces to finding subsets summing to exactly `Sum(P)`.
* Time: $O(N \times \text{Subset\_Sum})$.
* Space: $O(\text{Subset\_Sum})$ using 1D array.



### 5. Suggest Solutions

Prefer simple, clear, straight-forward implementations.
We will implement **Approach 2 (Recursion + Memoization)**. It directly translates the "by hand" decision tree in Step 3 into code, is highly readable, and avoids clever math tricks that are difficult to explain under pressure.

### 6. Outline Core Logic

```python
def findTargetSumWays(nums, target):
    """
    Reframe: Count paths in a binary decision tree (+/-) that land on target sum.
    State: Cache tracking (current_index, current_sum), chosen because subproblems heavily overlap (many branches reach same sum at same depth).
    Invariant: Number of ways to reach target from (index, sum) is constant.

    dfs(index, current_sum) = computes valid paths to target from current position.

    Core logic:
    - If end of array reached, check if current sum matches target.
    - If cache contains state, return cached integer.
    - Calculate ways if we add current number (recurse).
    - Calculate ways if we subtract current number (recurse).
    - Save sum of both branches to cache.
    - Return sum of branches.

    Edge cases:
    - target absolute value is greater than sum of all elements (impossible to reach).
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton**

```python
def findTargetSumWays(nums, target):
    def dfs(index, current_sum):
        # TO DO: Base case (end of array)
        # TO DO: Recursive branches (+ and -)
        pass
    
    return dfs(0, 0)

```

**Iteration 2: Core Logic Chunking**

```python
def findTargetSumWays(nums, target):
    def dfs(index, current_sum):
        # ADDED: Base case
        if index == len(nums):
            return 1 if current_sum == target else 0
        
        # ADDED: Recursive branches matching plain English outline
        add_ways = dfs(index + 1, current_sum + nums[index])
        sub_ways = dfs(index + 1, current_sum - nums[index])
        
        return add_ways + sub_ways
    
    return dfs(0, 0)

```

**Iteration 3: Adding Memoization (State Caching)**

```python
def findTargetSumWays(nums, target):
    memo = {} # ADDED: cache dict

    def dfs(index, current_sum):
        if index == len(nums):
            return 1 if current_sum == target else 0
            
        # ADDED: Check cache before branching
        if (index, current_sum) in memo:
            return memo[(index, current_sum)]
        
        add_ways = dfs(index + 1, current_sum + nums[index])
        sub_ways = dfs(index + 1, current_sum - nums[index])
        
        # ADDED: Save to cache before returning
        memo[(index, current_sum)] = add_ways + sub_ways
        return memo[(index, current_sum)]
    
    return dfs(0, 0)

```

**Iteration 4: Patching Edge Cases**

```python
def findTargetSumWays(nums, target):
    # ADDED: Edge case. Unreachable target bypasses recursion entirely.
    total_sum = sum(nums)
    if abs(target) > total_sum:
        return 0

    memo = {} 

    def dfs(index, current_sum):
        if index == len(nums):
            return 1 if current_sum == target else 0
            
        if (index, current_sum) in memo:
            return memo[(index, current_sum)]
        
        add_ways = dfs(index + 1, current_sum + nums[index])
        sub_ways = dfs(index + 1, current_sum - nums[index])
        
        memo[(index, current_sum)] = add_ways + sub_ways
        return memo[(index, current_sum)]
    
    return dfs(0, 0)

```

### 8. Complexity & Optimizations

**Commentary:** The memoization approach successfully prunes the exponential $O(2^N)$ time down to $O(N \times \text{Total\_Sum})$. However, space complexity is also $O(N \times \text{Total\_Sum})$ due to the dictionary and recursion stack. Hash map lookups can carry overhead.

**Optimization (Subset Sum DP):**
If asked to optimize memory, switch to the math approach. `Sum(P) = (target + Total) / 2`.
This eliminates recursion entirely and uses a 1D array.

```python
def findTargetSumWays_optimized(nums, target):
    total_sum = sum(nums)
    
    # Edge cases: target unreachable OR division by 2 leaves remainder
    if abs(target) > total_sum or (total_sum + target) % 2 != 0:
        return 0
        
    subset_target = (total_sum + target) // 2
    dp = [0] * (subset_target + 1)
    dp[0] = 1 # 1 way to make sum 0 (use no elements)
    
    for num in nums:
        for current_sum in range(subset_target, num - 1, -1):
            dp[current_sum] += dp[current_sum - num]
            
    return dp[subset_target]

```

Space drops to $O(\text{Subset\_Sum})$ and execution is faster due to contiguous memory array usage instead of hash dictionary lookups.