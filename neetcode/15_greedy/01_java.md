### 1. Restatement

We need to find a continuous sequence of numbers inside a given array that adds up to the largest possible total.

* **Given:** An array of integers.
* **Return:** A single integer representing the maximum sum of any contiguous subarray.
* **Constraints:** The subarray must be contiguous (elements next to each other) and non-empty (at least one element). Order is fixed by the array. Mutation is not required, as we are only reading the values.

### 2. Clarifying questions and assumptions

Before writing code, I would clarify a few details:

* **Can the array be empty?** The problem states "non-empty sequence," so I will assume `nums.length >= 1`.
* **Can all numbers be negative?** Yes. If the array is `[-3, -5, -2]`, the maximum subarray is `[-2]` with a sum of `-2`. We cannot return `0` (an empty subarray).
* **Will the maximum sum fit in a standard 32-bit signed integer?** I will assume yes, so returning an `int` is safe. If the array were massive and contained large integers, we might need a `long` to prevent overflow, but standard integer bounds are typical for this problem.
* **Do we need to return the actual subarray bounds?** No, just the maximum sum.

### 3. Manual example

Let's trace a representative input: `nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]`

At each step, we decide whether to add the current number to our running sequence, or abandon the previous sequence and start a new one right here.

* `nums[0] = -2`: Start sequence here. (Current sum = -2, Max overall = -2)
* `nums[1] = 1`: Should we append `1` to `-2` (sum = -1) or start fresh at `1` (sum = 1)? 1 is better. (Current sum = 1, Max = 1)
* `nums[2] = -3`: Append `-3` to `1` (sum = -2). Starting fresh is -3. -2 is better. (Current sum = -2, Max = 1)
* `nums[3] = 4`: Append `4` to `-2` (sum = 2). Starting fresh is 4. 4 is better. (Current sum = 4, Max = 4)
* `nums[4] = -1`: Append `-1` to `4` (sum = 3). Starting fresh is -1. 3 is better. (Current sum = 3, Max = 4)
* `nums[5] = 2`: Append `2` to `3` (sum = 5). (Current sum = 5, Max = 5)
* `nums[6] = 1`: Append `1` to `5` (sum = 6). (Current sum = 6, Max = 6)
* `nums[7] = -5`: Append `-5` to `6` (sum = 1). (Current sum = 1, Max = 6)
* `nums[8] = 4`: Append `4` to `1` (sum = 5). (Current sum = 5, Max = 6)

The final answer is 6.

### 4. Candidate solutions

**1. Brute Force (O(n²))**

* **Core idea:** Try every possible starting index `i`, and for each `i`, iterate through every ending index `j`, keeping a running sum. Record the maximum sum found.
* **Data structures:** Only primitive integers for the loops and maximum.
* **Complexity:** O(n²) time, O(1) space.
* **Tradeoffs:** Very easy to write and verify, but entirely too slow for large inputs.

**2. Divide and Conquer (O(n log n))**

* **Core idea:** Split the array in half. The maximum subarray must lie entirely in the left half, entirely in the right half, or crossing the midpoint. Recursively find the max in each half, and compute the crossing max, returning the best of the three.
* **Data structures:** Call stack for recursion.
* **Complexity:** O(n log n) time, O(log n) space.
* **Tradeoffs:** Overly complex to implement compared to simpler optimal solutions.

**3. Dynamic Programming / Kadane's Algorithm (O(n))**

* **Core idea:** As seen in the manual example, the maximum subarray ending at index `i` is either the element at `i` itself, or the element at `i` plus the maximum subarray ending at `i-1`.
* **Data structures:** Two integer variables to track the current running sum and the global maximum.
* **Complexity:** O(n) time, O(1) space.
* **Tradeoffs:** Optimal in both time and space. The only challenge is recognizing the state transition logic, but once understood, implementation is trivial.

### 5. Selected solution and justification

I will use **Kadane's Algorithm (Dynamic Programming)**. It is the simplest and most optimal solution. It easily handles all-negative arrays naturally and requires no extra memory allocations or complex data structures, satisfying the problem in a single O(n) pass.

### 6. Plain-English implementation outline

```java
int maxSubArray(int[] nums) {
    /*
     * Reframe:
     * Walk through the array deciding at each step whether to extend the previous 
     * subarray or start a new one. Keep track of the highest sum seen.
     *
     * State:
     * currentSum: the max subarray sum ending at the current element.
     * maxSum: the highest subarray sum seen anywhere so far.
     * Chosen because we only need local history (the step immediately prior) 
     * and global history (the best overall).
     *
     * Invariant:
     * At the end of index i, currentSum holds the best possible sum for a 
     * contiguous subarray that ends exactly at i.
     *
     * Core logic:
     * - initialize currentSum and maxSum using the first element
     * - loop from the second element to the end of the array
     * - update currentSum: it's the maximum of (the current number alone) 
     *   or (the current number + currentSum)
     * - update maxSum: it's the maximum of (maxSum) or (currentSum)
     * - return maxSum
     *
     * Edge cases:
     * - single-element array
     * - all negative elements
     */
}

```

### 7. Iterative Java implementation

**Iteration 1: method skeleton**

```java
int maxSubArray(int[] nums) {
    int currentSum = nums[0];
    int maxSum = nums[0];

    // TODO: loop from second element to the end
    // TODO: update currentSum
    // TODO: update maxSum

    return maxSum;
}

```

*I initialize the states with the first element (`nums[0]`). This safely anchors our tracking and assumes the array length is at least 1.*

**Iteration 2: implement the core loop**

```java
int maxSubArray(int[] nums) {
    int currentSum = nums[0];
    int maxSum = nums[0];

    for (int i = 1; i < nums.length; i++) {
        int currentElement = nums[i];
        
        // Added: State transition for the current running sum
        currentSum = Math.max(currentElement, currentSum + currentElement);

        // TODO: update maxSum
    }

    return maxSum;
}

```

*We loop starting at `i = 1`. At each step, `currentSum` becomes either the element itself (we start a new sequence) or the element appended to the previous sequence (we extend).*

**Iteration 3: complete the happy path**

```java
int maxSubArray(int[] nums) {
    int currentSum = nums[0];
    int maxSum = nums[0];

    for (int i = 1; i < nums.length; i++) {
        int currentElement = nums[i];
        
        currentSum = Math.max(currentElement, currentSum + currentElement);
        // Added: Track the highest sum we've ever achieved
        maxSum = Math.max(maxSum, currentSum);
    }

    return maxSum;
}

```

**Edge-case pass**
Let's review the edge cases identified:

* *Array with one element (`nums = [5]`):* The loop `for (int i = 1; i < 1)` won't execute. It immediately returns `maxSum`, which was initialized to `5`. Correct.
* *All negative array (`nums = [-3, -5, -2]`):*
* `i=0`: current = -3, max = -3.
* `i=1`: currentElement = -5. `Math.max(-5, -3 + -5)` -> `-5`. `max` remains `-3`.
* `i=2`: currentElement = -2. `Math.max(-2, -5 + -2)` -> `-2`. `max` becomes `-2`.
* Returns `-2`. Correct.



No code modifications are necessary. The algorithm gracefully handles these natively.

### 8. Final code

```java
class Solution {
    public int maxSubArray(int[] nums) {
        int currentSum = nums[0];
        int maxSum = nums[0];

        for (int i = 1; i < nums.length; i++) {
            int currentElement = nums[i];
            
            // Decide to either extend the existing subarray or start a new one
            currentSum = Math.max(currentElement, currentSum + currentElement);
            
            // Record the maximum sum found so far
            maxSum = Math.max(maxSum, currentSum);
        }

        return maxSum;
    }
}

```

### 9. Complexity

* **Time Complexity:** O(n). We perform exactly one pass over the input array, where `n` is the length of `nums`. Each step inside the loop takes O(1) time.
* **Space Complexity:** O(1). We only store a few primitive variables (`currentSum`, `maxSum`, `currentElement`), requiring no extra scaling memory.

### 10. Brief test walkthrough

* **Main Example:** `nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]`
* As tested manually earlier, `currentSum` resets at `4`, dips to `3`, peaks at `6` before the `-5`, and `maxSum` locks in that `6`. Expected: `6`.


* **Smallest valid input:** `nums = [1]`
* `currentSum` and `maxSum` init to `1`. Loop doesn't run. Expected: `1`.


* **All negative case:** `nums = [-5, -2, -9]`
* `currentSum` defaults to `-5`. At `-2`, `Math.max(-2, -7)` sets `currentSum = -2`. `maxSum = -2`. At `-9`, `Math.max(-9, -11)` sets `currentSum = -9`. `maxSum` remains `-2`. Expected: `-2`.