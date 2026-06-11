## question
You are given an array of positive integers nums.
Return true if you can partition the array into two subsets, subset1 and subset2 where sum(subset1) == sum(subset2). Otherwise, return false.

### 1. Restate

Given array of positive integers. Check if possible to split into two groups where sum of group A equals sum of group B.

### 2. Clarify

* **Input:** Array `nums`, `[1, 5, 11, 5]`. Always positive integers.
* **Output:** Boolean. `True` if equal partition exists, `False` otherwise.
* **Questions:**
* Can array be empty or 1 element? *Assume length >= 1.*
* What if total sum is odd? *Impossible to split evenly. Fast fail.*



### 3. By-Hand Example

Input: `[1, 5, 11, 5]`
Total sum = 22. Target per group = 11.
Track reachable sums:

* Start: `{0}`
* Process `1`: Add 1 to all. New sums: `{0, 1}`
* Process `5`: Add 5 to all. New sums: `{0, 1, 5, 6}`
* Process `11`: Add 11 to all. New sums: `{0, 1, 5, 6, 11, 12, 16, 17}`
* Target 11 found. Return `True`.

### 4. Brainstorm & Complexity

* **Brute Force (Recursion):** Try every element in subset 1 or 2. Time O(2^n). Space O(n) call stack. Too slow.
* **Memoized DFS:** State `(index, current_sum)`. Time O(N * Target). Space O(N * Target). Good, but recursive overhead.
* **Iterative DP (Set/Reachability):** Maintain set of possible sums. Add current number to all previous sums. Time O(N * Target). Space O(Target). Directly maps to hand-computation.

### 5. Suggest Solutions

Prefer Iterative DP (Reachability Set). It directly implements the by-hand example from step 3. It’s conceptually simple: "keep track of every sum we can build; if we build the target, we win."

### 6. Outline & Logic

```python
def can_partition(nums):
    """
    Reframe: Find if any subset sums exactly to total_sum / 2.
    State: A set of reachable sums, chosen because we only care about unique sums formed, not how we formed them.
    Invariant: The set contains all valid subset sums using elements processed so far.

    helperName(args) = N/A

    Core logic:
    - calculate target sum (total / 2)
    - init reachable sums collection with 0
    - for each number in input:
        - create new sums by adding number to every existing reachable sum
        - merge new sums into reachable sums collection
        - if target exists in reachable sums, return true
    - return false if loop finishes without hitting target

    Edge cases:
    - total sum is odd (impossible to reach integer half)
    - generated sum exceeds target (useless, wastes memory)
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton**

```python
def can_partition(nums):
    # calculate target
    # init reachable_sums
    # for each num:
        # generate new_sums
        # merge into reachable_sums
        # check target
    # return False

```

**Iteration 2: Core Logic Chunking**
*Turning plain English to code.*

```python
def can_partition(nums):
    total_sum = sum(nums)
    target = total_sum // 2
    
    reachable_sums = {0}
    
    for num in nums:
        new_sums = set()
        for current in reachable_sums:
            new_sums.add(current + num)
            
        reachable_sums.update(new_sums) # merge
        
        if target in reachable_sums:
            return True
            
    return False

```

**Iteration 3: Patching Edge Cases**
*Addressing odd sums and capping sums to save memory/time.*

```python
def can_partition(nums):
    total_sum = sum(nums)
    
    # PATCH 1: Odd total sum edge case
    if total_sum % 2 != 0:
        return False
        
    target = total_sum // 2
    reachable_sums = {0}
    
    for num in nums:
        new_sums = set()
        for current in reachable_sums:
            # PATCH 2: Cap at target (ignore elements > target)
            if current + num <= target:
                new_sums.add(current + num)
                
        reachable_sums.update(new_sums)
        
        if target in reachable_sums:
            return True
            
    return False

```

### 8. Complexity & Optimizations

* **Time Complexity:** O(N * Target). Inner loop runs at most `Target` times per number.
* **Space Complexity:** O(Target). The set stores at most `Target + 1` elements.
* **Optimization Comment:** Set iteration can have overhead. In languages like Python or C++, you can use **Bit Manipulation**. Treat the set as a binary number where the `i-th` bit represents if sum `i` is reachable.
* *Bitmask Optimization:* `reachable = reachable | (reachable << num)`
* This reduces space to O(Target / 64) and makes the inner loop an O(1) bitwise shift operation, vastly improving runtime constant factors while maintaining identical logic.