## question:
You are given an integer array nums where nums[i] represents the amount of money the ith house has. The houses are arranged in a circle, i.e. the first house and the last house are neighbors.
You are planning to rob money from the houses, but you cannot rob two adjacent houses because the security system will automatically alert the police if two adjacent houses were both broken into.
Return the maximum amount of money you can rob without alerting the police.

## 1. Restating the Question

We need to find the maximum money we can steal from a row of houses. The catch? The houses form a circle. If you rob two houses next to each other, alarms go off. Since it's a circle, the first and last houses are considered neighbors.

## 2. Clarifying Questions & Inputs/Outputs

* **Q:** Can the money amounts be negative?
* **A:** Assume non-negative integers.
* **Q:** What if there is only 1 house? Or 0?
* **A:** If 0 houses, return 0. If 1 house, return its value.
* **Inputs:** `nums: List[int]`
* **Outputs:** `int` (Max money stolen)

---

## 3. Hand-Tracing an Example

Let's trace `nums = [1, 2, 3, 1]`

Because house 0 (value 1) and house 3 (value 1) are neighbors, we can't rob both. We split this into two simpler linear options:

1. **Option A (Ignore last house):** `[1, 2, 3]`
* Rob 1 -> total 1
* Rob 2 -> max(2, 1) = 2
* Rob 3 -> max(3 + 1, 2) = 4
* Total for Option A = 4


2. **Option B (Ignore first house):** `[2, 3, 1]`
* Rob 2 -> total 2
* Rob 3 -> max(3, 2) = 3
* Rob 1 -> max(1 + 2, 3) = 3
* Total for Option B = 3



Max of both options is **4**.

---

## 4. Brainstorming & Complexity

* **Brute Force:** Try every valid combination of houses. For $N$ houses, checking all subsets without adjacent elements takes $O(2^N)$ time. Way too slow.
* **Dynamic Programming (Linear):** For a straight line of houses, at each house we decide: rob it (and add to profit from two houses ago) or skip it (keep profit from previous house). This takes $O(N)$ time and $O(1)$ space if we only keep track of the last two profits.
* **Handling the Circle:** The circular constraint means we can never choose both the first and last house. So, we can just run the linear logic twice: once skipping the first house, and once skipping the last house. The answer is the max of these two runs.

---

## 5. Suggested Solution

We will use the **Linear DP Split approach**. It's clean, avoids tracking complex circular indices, and reuses the classic House Robber logic.

---

## 6. Outline of Selected Implementation

```python
def rob(nums):
    """
    Reframe: A circular robber problem is just two linear robber problems: one without the first house, one without the last.
    State: 'prev_max' and 'curr_max' tracking profits, chosen because we only need the history of the last two houses.
    Invariant: At each step, 'curr_max' stores the absolute max profit possible up to the current house.

    linear_rob(sub_houses) = computes max profit for a straight line of houses.

    Core logic:
    - Slice the input into two lists: one missing the first element, one missing the last element.
    - Run the linear robbery helper on both lists.
    - Return the larger total of the two results.

    Edge cases:
    - Empty array -> return 0
    - Only 1 house -> return that house value
    - 2 or 3 houses -> covered correctly by the logic splits
    """

```

---

## 7. Iterative Implementation

### Iteration 1: The Skeleton (Stubs & Core Logic)

Let's build the high-level flow first using placeholders for the linear calculation.

```python
def rob(nums):
    # Skeleton representing our plain English core logic
    
    def linear_rob(sub_vals):
        # TODO: Implement linear house robber logic
        pass
        
    # Split into two lines
    option_1 = nums[1:]  # Exclude first
    option_2 = nums[:-1] # Exclude last
    
    # Return the max of both paths
    return max(linear_rob(option_1), linear_rob(option_2))

```

### Iteration 2: Implementing the Core Helper Logic

Now, let's fill in the `linear_rob` helper using standard DP with constant space.

```python
def rob(nums):
    def linear_rob(sub_vals):
        prev_max = 0
        curr_max = 0
        for val in sub_vals:
            # Decide: rob current house + two-steps-ago profit, or skip current house
            temp = max(curr_max, prev_max + val)
            prev_max = curr_max
            curr_max = temp
        return curr_max
        
    option_1 = nums[1:]
    option_2 = nums[:-1]
    
    return max(linear_rob(option_1), linear_rob(option_2))

```

### Iteration 3: Patching Edge Cases

The core logic works fine for multiple houses, but what if `nums` only has 1 house? If `nums = [5]`, `nums[1:]` is `[]` and `nums[:-1]` is `[]`. Both yield 0, which is wrong. We need to handle small inputs.

```python
def rob(nums):
    # Edge case patch: 1 house cannot be split into two valid subarrays
    if len(nums) == 1:
        return nums[0]
    if not nums:
        return 0

    def linear_rob(sub_vals):
        prev_max = 0
        curr_max = 0
        for val in sub_vals:
            temp = max(curr_max, prev_max + val)
            prev_max = curr_max
            curr_max = temp
        return curr_max
        
    option_1 = nums[1:]
    option_2 = nums[:-1]
    
    return max(linear_rob(option_1), linear_rob(option_2))

```

---

## 8. Complexity & Optimization

* **Time Complexity:** $O(N)$. We iterate through the array elements twice (once for each slice). $O(2N)$ simplifies to $O(N)$.
* **Space Complexity:** $O(N)$ due to Python slicing (`nums[1:]` creates a copy).

### Optimization to $O(1)$ Space

Instead of copying arrays with slicing, we can pass index boundaries (`start`, `end`) to our helper function to keep space completely constant.

```python
def rob(nums):
    if len(nums) == 1:
        return nums[0]
        
    def linear_rob(start, end):
        prev_max = 0
        curr_max = 0
        for i in range(start, end):
            temp = max(curr_max, prev_max + nums[i])
            prev_max = curr_max
            curr_max = temp
        return curr_max
    
    # Run from index 1 to N-1, and index 0 to N-2
    return max(linear_rob(1, len(nums)), linear_rob(0, len(nums) - 1))

```

* **Final Time:** $O(N)$
* **Final Space:** $O(1)$