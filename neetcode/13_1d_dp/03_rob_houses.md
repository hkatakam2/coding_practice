## question
You are given an integer array nums where nums[i] represents the amount of money the ith house has. The houses are arranged in a straight line, i.e. the ith house is the neighbor of the (i-1)th and (i+1)th house.
You are planning to rob money from the houses, but you cannot rob two adjacent houses because the security system will automatically alert the police if two adjacent houses were both broken into.
Return the maximum amount of money you can rob without alerting the police.

## 1. Restating the Question

We need to find the maximum amount of money you can steal from a line of houses. The only constraint is that you cannot rob two consecutive houses, or the alarm triggers.

---

## 2. Clarifying Questions & Inputs/Outputs

* **Inputs:** `nums`: List[int], where `nums[i]` is the cash in house `i`.
* **Outputs:** `int`, the maximum total cash possible.
* **Constraints & Assumptions:** * Can `nums` be empty? (Assume yes, or contains at least 1 element).
* Can house values be negative? (Assume values $\ge 0$).
* Array size fits in memory.



---

## 3. Hand-Tracing an Example

Let's trace `nums = [2, 7, 9, 3, 1]`

* **House 0 (2):** Max cash if we stop here = **2**
* **House 1 (7):** Max cash is either rob this one (7) or keep previous (2) = **7**
* **House 2 (9):** Rob this (9 + House 0's cash = 11) or skip (House 1's cash = 7) = **11**
* **House 3 (3):** Rob this (3 + House 1's cash = 10) or skip (House 2's cash = 11) = **11**
* **House 4 (1):** Rob this (1 + House 2's cash = 12) or skip (House 3's cash = 11) = **12**

**Final Output:** 12

---

## 4. Brainstorming & Complexity

* **Brute Force (Decision Tree):** For each house, choices are rob or skip. This yields $O(2^n)$ time due to branching, and $O(n)$ space for the recursion stack. Way too slow.
* **Dynamic Programming (Array):** We can cache subproblem results. To find the max cash at house `i`, look at `max_cash[i-1]` (skip current) vs `nums[i] + max_cash[i-2]` (rob current). $O(n)$ time, $O(n)$ space.
* **DP (Space Optimized):** Notice we only ever look back two steps. We can replace the DP array with just two variables tracking the running totals. $O(n)$ time, $O(1)$ space.

---

## 5. Suggested Solution

We will go with the **Space-Optimized DP** approach. It matches our manual trace directly, runs in linear time, uses constant memory, and is highly readable.

---

## 6. Implementation Outline

```python
def rob(nums: list[int]) -> int:
    """
    Reframe: Maximize non-adjacent sum via sequential local choices.
    State: cash_two_houses_ago, cash_one_house_ago maintained because they represent the only historical context needed to make the current decision.
    Invariant: At each step, cash_one_house_ago holds the maximum possible loot up to the previous house.

    Core logic:
    - Loop through each house value in the input list
    - For the current house, calculate the potential loot if robbed (current value + cash_two_houses_ago)
    - Determine the best choice by taking the maximum between robbing the current house and skipping it (cash_one_house_ago)
    - Shift the historical states forward for the next iteration
    
    Edge cases:
    - Empty input list (return 0)
    - Single house in the list (return that house's value)
    """

```

---

## 7. Iterative Implementation

### Iteration 1: Skeleton & Core Logic (Happy Path)

We focus purely on the iterative loop mechanism using placeholder variables.

```python
def rob(nums: list[int]) -> int:
    # SKELETON: Core loop processing houses
    cash_two_houses_ago = 0
    cash_one_house_ago = 0
    
    for loot in nums:
        # Calculate options
        rob_current = loot + cash_two_houses_ago
        skip_current = cash_one_house_ago
        
        # Pick the best option
        current_max = max(rob_current, skip_current)
        
        # TODO: Shift states forward for next loop iteration
        
    return cash_one_house_ago

```

### Iteration 2: Realizing State Shifts

Now we fill in the state tracking details inside the loop.

```python
def rob(nums: list[int]) -> int:
    cash_two_houses_ago = 0
    cash_one_house_ago = 0
    
    for loot in nums:
        rob_current = loot + cash_two_houses_ago
        skip_current = cash_one_house_ago
        
        current_max = max(rob_current, skip_current)
        
        # UPDATE: Advancing our historical windows
        cash_two_houses_ago = cash_one_house_ago
        cash_one_house_ago = current_max
        
    return cash_one_house_ago

```

### Iteration 3: Patching Edge Cases

The core logic works fine for normal lists, but we need to verify explicit empty or minimal inputs. If `nums` is empty, the loop won't execute and returns `0` (which is correct). If `nums` has 1 item, it evaluates `max(loot + 0, 0)`, updates correctly, and returns the single item.

Let's clean it up slightly for production readiness.

```python
def rob(nums: list[int]) -> int:
    # EDGE CASE: Explicit check for empty list to exit early
    if not nums:
        return 0
        
    cash_two_houses_ago = 0
    cash_one_house_ago = 0
    
    for loot in nums:
        # Optimized variable updates inline
        current_max = max(loot + cash_two_houses_ago, cash_one_house_ago)
        cash_two_houses_ago = cash_one_house_ago
        cash_one_house_ago = current_max
        
    return cash_one_house_ago

```

---

## 8. Complexity & Optimization

* **Time Complexity:** $O(n)$ where $n$ is the number of houses. We iterate through the list exactly once.
* **Space Complexity:** $O(1)$ constant space. We only store two integer variables tracking the historical maximums, avoiding allocating any array structures.