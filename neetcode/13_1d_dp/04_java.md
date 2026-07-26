### 1. Restate the problem

We have a list of houses, each containing a certain amount of money, arranged in a circle. This means the very first house and the very last house are adjacent to each other. We want to find the maximum total amount of money we can collect without ever choosing two houses that are adjacent.

**Given:** An integer array `nums` representing the money in each house.
**Return:** An integer representing the maximum money we can rob.
**Constraint:** We cannot pick `nums[i]` and `nums[i+1]`. Because of the circle, we also cannot pick `nums[0]` and `nums[n-1]`.

### 2. Ask clarifying questions

Before writing code, I would confirm a few assumptions with you:

* **Input size:** What is the possible length of `nums`? Can it be empty or have just one house? (I will assume length $\ge 1$).
* **Value bounds:** Are the amounts of money always non-negative? (I will assume $\ge 0$).
* **Integer overflow:** Will the maximum possible sum fit within a standard 32-bit signed `int`? (I will assume yes, but if there are millions of houses with large amounts, we might need a `long`. I'll use `int` for now).
* **Mutation:** Do I need to preserve the `nums` array? (My approach won't modify it anyway).

### 3. Work through an example by hand

Let's trace an example: `nums = [1, 2, 3, 1]`.
The circle means indices 0, 1, 2, 3 wrap around so 0 and 3 are adjacent.

* If I decide to rob House 0 (`1`), I **cannot** rob House 1 (`2`) and I **cannot** rob House 3 (`1`).
* Available houses left: House 2 (`3`).
* Max for this scenario: `1 + 3 = 4`.


* If I decide **not** to rob House 0, I am free to consider House 3.
* Available houses: House 1 (`2`), House 2 (`3`), House 3 (`1`).
* If I rob House 1 (`2`), I can't rob House 2. I can rob House 3 (`1`). Total = `3`.
* If I rob House 2 (`3`), I can't rob House 1 or 3. Total = `3`.


* The overall maximum is `4`.

### 4. Brainstorm solutions aloud

* **Direct Simulation (Brute Force):** I could use recursion to try picking or skipping each house, wrapping around at the end to ensure house 0 and house $n-1$ aren't both selected. This would take $O(2^n)$ time, which is too slow.
* **Dynamic Programming (Linear):** If the houses were in a straight line, I could solve this in $O(n)$ time. At any house $i$, the max money is the maximum of:
1. Skipping house $i$: the max money up to $i-1$.
2. Robbing house $i$: the max money up to $i-2$ plus the money at house $i$.


* **Dynamic Programming (Circular):** Because the array is a circle, the only new restriction is that we cannot rob *both* the first and the last house.
This means the optimal solution must fall into one of two categories:
1. We *might* rob the first house, which guarantees we absolutely *cannot* rob the last house. The problem simplifies to a linear array from index $0$ to $n-2$.
2. We *might* rob the last house, which guarantees we absolutely *cannot* rob the first house. The problem simplifies to a linear array from index $1$ to $n-1$.
If we solve both of these linear DP scenarios, the overall answer is just the maximum of the two results.



### 5. Select the solution

I will use the **Circular Dynamic Programming** approach. It allows us to reuse the standard $O(n)$ linear solution twice.
By maintaining only the previous two states (`prev2` and `prev1`) instead of allocating a whole DP array, I can reduce the space complexity to $O(1)$. This is optimal, easy to explain, and avoids complex wraparound index arithmetic.

### 6. Write the implementation outline

```java
int rob(int[] nums) {
    /*
     * Reframe:
     * A circular rob is just the maximum of two linear robs: 
     * one excluding the last house, and one excluding the first house.
     *
     * State:
     * - Two integer variables (prev1, prev2) for the linear subproblems.
     * Chosen because:
     * - We only ever look back exactly 1 and 2 steps, so an entire DP array is wasted space.
     *
     * Invariant:
     * prev1 holds the max money robbed up to the immediately preceding house.
     * prev2 holds the max money robbed up to two houses ago.
     *
     * Helpers:
     * robLinear(nums, start, end)
     * - computes the max money we can rob in a straight line between the start and end indices.
     *
     * Core logic:
     * - if the array has only 1 element, return it.
     * - calculate max1 by calling robLinear from house 0 to n-2.
     * - calculate max2 by calling robLinear from house 1 to n-1.
     * - return the maximum of max1 and max2.
     *
     * Edge cases:
     * - array of length 1 (start and end bounds would cross in the split).
     * - array of length 2 (handled correctly by the linear helper).
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton**
I'll create the main control flow and a stub for the linear helper.

```java
public int rob(int[] nums) {
    if (nums.length == 1) {
        return nums[0];
    }
    
    // TODO: rob from 0 to n-2
    // TODO: rob from 1 to n-1
    // TODO: return the max of both
    return 0;
}

private int robLinear(int[] nums, int start, int end) {
    return 0; // TODO: implement standard linear house robber
}

```

**Iteration 2: Implement the easiest core section (the helper)**
Now I'll implement `robLinear`. As I iterate from `start` to `end`, I'll track the max money up to $i-2$ (`robbedTwoBefore`) and up to $i-1$ (`robbedOneBefore`).

```java
public int rob(int[] nums) {
    if (nums.length == 1) {
        return nums[0];
    }
    
    // TODO: main method calls
    return 0;
}

private int robLinear(int[] nums, int start, int end) {
    int robbedTwoBefore = 0;
    int robbedOneBefore = 0;
    
    for (int i = start; i <= end; i++) {
        // Option 1: rob this house + whatever we had 2 houses ago.
        // Option 2: skip this house, keep whatever we had 1 house ago.
        int currentMax = Math.max(robbedTwoBefore + nums[i], robbedOneBefore);
        
        // Shift variables forward for the next iteration.
        robbedTwoBefore = robbedOneBefore;
        robbedOneBefore = currentMax;
    }
    
    // The max at the end of the segment is stored here.
    return robbedOneBefore;
}

```

**Iteration 3: Complete the happy path**
Now I will wire up the main method to invoke the linear helper for both valid ranges.

```java
public int rob(int[] nums) {
    if (nums.length == 1) {
        return nums[0];
    }
    
    int n = nums.length;
    
    // Added: call helper for index 0 to n-2
    int maxExcludingLast = robLinear(nums, 0, n - 2);
    
    // Added: call helper for index 1 to n-1
    int maxExcludingFirst = robLinear(nums, 1, n - 1);
    
    // Added: return the best of the two scenarios
    return Math.max(maxExcludingLast, maxExcludingFirst);
}

private int robLinear(int[] nums, int start, int end) {
    int robbedTwoBefore = 0;
    int robbedOneBefore = 0;
    
    for (int i = start; i <= end; i++) {
        int currentMax = Math.max(robbedTwoBefore + nums[i], robbedOneBefore);
        robbedTwoBefore = robbedOneBefore;
        robbedOneBefore = currentMax;
    }
    
    return robbedOneBefore;
}

```

**Edge-case pass**
Let's verify the edge cases noted earlier:

* `nums.length == 1`: The main method catches this immediately and returns `nums[0]`. Without this check, `n-2` would be `-1`, and `robLinear` would be called with `start=0, end=-1`.
* `nums.length == 2`:
* `maxExcludingLast` calls `robLinear(0, 0)`. Loop runs once, returning `nums[0]`.
* `maxExcludingFirst` calls `robLinear(1, 1)`. Loop runs once, returning `nums[1]`.
* Returns `Math.max(nums[0], nums[1])`. This is perfectly correct since we can only pick one of the two houses.


* Array elements are 0: Math will correctly process 0. No issues.

### Final Code

The code is clean, handles the constraints, and doesn't require any unnecessary variables.

```java
class Solution {
    public int rob(int[] nums) {
        if (nums == null || nums.length == 0) {
            return 0;
        }
        if (nums.length == 1) {
            return nums[0];
        }
        
        int n = nums.length;
        int maxExcludingLast = robLinear(nums, 0, n - 2);
        int maxExcludingFirst = robLinear(nums, 1, n - 1);
        
        return Math.max(maxExcludingLast, maxExcludingFirst);
    }

    private int robLinear(int[] nums, int start, int end) {
        int robbedTwoBefore = 0;
        int robbedOneBefore = 0;
        
        for (int i = start; i <= end; i++) {
            int currentMax = Math.max(robbedTwoBefore + nums[i], robbedOneBefore);
            robbedTwoBefore = robbedOneBefore;
            robbedOneBefore = currentMax;
        }
        
        return robbedOneBefore;
    }
}

```

### Complexity

* **Time Complexity:** $O(n)$. We iterate through the array roughly twice (once from $0$ to $n-2$, and once from $1$ to $n-1$). Traversing $2n$ elements simplifies to $O(n)$ linear time.
* **Space Complexity:** $O(1)$. We only allocate a few primitive integer variables (`robbedTwoBefore`, `robbedOneBefore`, `currentMax`) regardless of the size of the input array.

### Brief test walkthrough

Let's test our final code with `nums = [2, 3, 2]`.

1. Length is 3. We split into two linear checks.
2. `robLinear(nums, 0, 1)` -> Array segment `[2, 3]`.
* `i = 0`: `currentMax = max(0 + 2, 0) = 2`. `twoBefore = 0`, `oneBefore = 2`.
* `i = 1`: `currentMax = max(0 + 3, 2) = 3`. `twoBefore = 2`, `oneBefore = 3`.
* Returns `3`.


3. `robLinear(nums, 1, 2)` -> Array segment `[3, 2]`.
* `i = 1`: `currentMax = max(0 + 3, 0) = 3`. `twoBefore = 0`, `oneBefore = 3`.
* `i = 2`: `currentMax = max(0 + 2, 3) = 3`. `twoBefore = 3`, `oneBefore = 3`.
* Returns `3`.


4. `Math.max(3, 3)` returns `3`.
Matches manual logic, the code succeeds.