### 1. Restate the problem

Given an array of integers, we need to find a continuous block of numbers that, when multiplied together, gives the highest possible product. We must return that maximum product.

The main twist is that the array can contain negative numbers and zeroes. Multiplying by a negative number shrinks the product, but multiplying by *another* negative number makes it positive again. Zeroes effectively "break" the product and force a reset. The output is guaranteed to fit within a standard 32-bit integer.

### 2. Ask clarifying questions

Before writing code, I would confirm a few assumptions:

* **Can the input array be empty or null?**
*Assumption:* The problem states the sequence is "non-empty," so we can assume the array has at least one element.
* **Are there constraints on intermediate values overflowing?**
*Assumption:* Since the final answer is guaranteed to fit in a 32-bit integer, I will assume intermediate subarray products also fit within standard integer bounds and `int` will suffice.
* **Are we allowed to modify the array?**
*Assumption:* We only need to read the array, so we won't modify the input in place.

### 3. Work through an example by hand

Let's trace a representative array: `nums = [2, -5, -2, -4, 3]`

* **Start at index 0 (`2`):**
* The max product so far is `2`. The min product is `2`.
* Best overall: `2`.


* **Index 1 (`-5`):**
* If we continue the subarray: `2 * -5 = -10`.
* If we start fresh: `-5`.
* The max product ending here is `-5`. The min product ending here is `-10`.
* Best overall remains `2`.


* **Index 2 (`-2`):**
* We have a negative number. Multiplying it by the previous *minimum* (which is negative) might give a huge positive.
* Continuing the previous max: `-5 * -2 = 10`.
* Continuing the previous min: `-10 * -2 = 20`.
* Starting fresh: `-2`.
* The max ending here is `20`. The min ending here is `-2`.
* Best overall updates to `20`.


* **Index 3 (`-4`):**
* Continuing max: `20 * -4 = -80`.
* Continuing min: `-2 * -4 = 8`.
* Starting fresh: `-4`.
* The max ending here is `8`. Min ending here is `-80`.
* Best overall remains `20`.


* **Index 4 (`3`):**
* Continuing max: `8 * 3 = 24`.
* Continuing min: `-80 * 3 = -240`.
* Starting fresh: `3`.
* The max ending here is `24`. Min ending here is `-240`.
* Best overall updates to `24`.



The maximum product is `24` (from subarray `[-2, -4, 3]`).

### 4. Brainstorm solutions aloud

**Option 1: Brute Force**
The most direct approach is to check every possible subarray using nested loops. For every starting index `i`, loop through every ending index `j`, multiply the numbers, and keep track of the maximum.

* *Time Complexity:* O(n²) where n is the array length.
* *Space Complexity:* O(1).
* *Tradeoffs:* Very easy to implement, but far too slow for large inputs.

**Option 2: Dynamic Programming (Tracking Min and Max)**
As seen in the manual example, the maximum product ending at a specific position depends on the previous position. Because a negative number can turn a small negative product into a massive positive one, we must track *both* the maximum and minimum continuous products ending at the previous step.
For each new number, the new maximum and minimum can only come from three places:

1. The number itself (starting a new subarray).
2. The previous maximum multiplied by the number.
3. The previous minimum multiplied by the number.

* *Time Complexity:* O(n), as we only need one pass through the array.
* *Space Complexity:* O(1), since we only need to remember the min, max, and best overall products for the immediate previous step.

### 5. Select the solution

I will use the **Dynamic Programming** approach tracking the min and max. It provides optimal O(n) time and O(1) space. It perfectly handles the problem's trickiest properties:

* Two negative numbers multiplying to a positive (handled by tracking the minimum).
* Zeroes resetting the sequence (handled by comparing the current number against the continuous product; `max(0, current * max)` will pick `0`, natively resetting the state).

### 6. Write the implementation outline

```java
int maxProduct(int[] nums) {
    /*
     * Reframe:
     * Walk through the array once, tracking the largest and smallest possible 
     * continuous products ending at the current position.
     *
     * State:
     * Three integers: the maximum product ending at the current step, the minimum 
     * product ending at the current step, and the absolute best product seen overall.
     * Chosen because tracking the minimum safely stores large negative accumulations
     * that might flip to positive later.
     *
     * Invariant:
     * After processing index i, currentMax and currentMin represent the highest and 
     * lowest subarray products that explicitly end at index i.
     *
     * Core logic:
     * - initialize our max, min, and best trackers using the first element
     * - loop through the remaining elements
     * - if the current number is negative, swapping the previous max and min simplifies 
     *   the math (since multiplying a max by a negative makes it a min)
     * - calculate the new max by choosing either the current number alone or the current 
     *   number extended by the previous max
     * - calculate the new min similarly
     * - update the overall best product if the new max is higher
     *
     * Edge cases:
     * - single element arrays
     * - zeroes resetting the product
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton**
First, I will set up the main loop and variables. At this stage, I am just planning the iteration and the global tracker.

```java
public int maxProduct(int[] nums) {
    int bestProduct = nums[0];
    
    // TODO: Track running min and max products
    
    for (int i = 1; i < nums.length; i++) {
        int current = nums[i];
        
        // TODO: Compute the max and min ending at 'current'
        
        // TODO: Update bestProduct
    }
    
    return bestProduct;
}

```

**Iteration 2: Adding the positive-only happy path**
Next, I will add the logic to track the running maximum and update the global best. This handles arrays with only positive numbers.

```java
public int maxProduct(int[] nums) {
    int bestProduct = nums[0];
    int currentMax = nums[0];
    
    for (int i = 1; i < nums.length; i++) {
        int current = nums[i];
        
        // Added: Calculate if we should start fresh or extend the current subarray
        currentMax = Math.max(current, currentMax * current);
        
        // Added: Update global best
        bestProduct = Math.max(bestProduct, currentMax);
    }
    
    return bestProduct;
}

```

**Iteration 3: Completing the core logic (handling negatives)**
Now, I will introduce `currentMin`. When `current` is negative, it flips the math: multiplying a large positive number by a negative makes it very small, while multiplying a large negative number by a negative makes it very large. A clean way to handle this is to swap `currentMax` and `currentMin` whenever we encounter a negative number.

```java
public int maxProduct(int[] nums) {
    int bestProduct = nums[0];
    int currentMax = nums[0];
    int currentMin = nums[0]; // State added to preserve negative potentials
    
    for (int i = 1; i < nums.length; i++) {
        int current = nums[i];
        
        // Added: When current is negative, the highest possible product 
        // will come from multiplying it with the lowest (most negative) previous product.
        if (current < 0) {
            int temp = currentMax;
            currentMax = currentMin;
            currentMin = temp;
        }
        
        currentMax = Math.max(current, currentMax * current);
        currentMin = Math.min(current, currentMin * current);
        
        bestProduct = Math.max(bestProduct, currentMax);
    }
    
    return bestProduct;
}

```

**Edge-case pass**

* *Single element:* `[3]`. The loop `i = 1` is skipped. Returns `3`. Correct.
* *Contains Zero:* `[-1, 0, -2]`.
* Starts at `-1`.
* At `0`: `currentMax = max(0, -1*0) = 0`, `currentMin = 0`. Best updates to `0`.
* At `-2`: `currentMax = max(-2, 0) = 0`, `currentMin = -2`. Best is `0`. Correct.


* *All negatives:* `[-2, -3, -4]`.
* `i=0`: max=-2, min=-2.
* `i=1 (-3)`: swap min/max. max = max(-3, 6) = 6. min = min(-3, 6) = -3. best = 6.
* `i=2 (-4)`: swap min/max. max = max(-4, 12) = 12. min = min(-4, -24) = -24. best = 12. (Subarray `[-3, -4]`). Correct.



### 8. Analyze expensive sections and optimize

There are no nested loops, sorts, or excessive object creations here. We are performing a single pass over primitive integers with standard library math operations.

* **Time Complexity:** O(N), where N is the length of `nums`. We visit each element exactly once.
* **Space Complexity:** O(1). We use a constant amount of extra space (three integer variables) regardless of the size of the input array.

### Final Code

```java
public int maxProduct(int[] nums) {
    int bestProduct = nums[0];
    int currentMax = nums[0];
    int currentMin = nums[0];
    
    for (int i = 1; i < nums.length; i++) {
        int current = nums[i];
        
        if (current < 0) {
            int temp = currentMax;
            currentMax = currentMin;
            currentMin = temp;
        }
        
        currentMax = Math.max(current, currentMax * current);
        currentMin = Math.min(current, currentMin * current);
        
        bestProduct = Math.max(bestProduct, currentMax);
    }
    
    return bestProduct;
}

```

### Brief test walkthrough

Let's quickly run the classic array `[2, 3, -2, 4]` through the final code:

* `i = 0`: `nums[0] = 2`. `bestProduct` = 2, `currentMax` = 2, `currentMin` = 2.
* `i = 1`: `current = 3`. Positive. `currentMax` = max(3, 6) = 6. `currentMin` = min(3, 6) = 3. `bestProduct` = 6.
* `i = 2`: `current = -2`. Negative, so swap `currentMax` (6) and `currentMin` (3). `currentMax` becomes 3, `currentMin` becomes 6.
* `currentMax` = max(-2, 3 * -2) = -2.
* `currentMin` = min(-2, 6 * -2) = -12.
* `bestProduct` = max(6, -2) = 6.


* `i = 3`: `current = 4`. Positive.
* `currentMax` = max(4, -2 * 4) = 4.
* `currentMin` = min(4, -12 * 4) = -48.
* `bestProduct` = max(6, 4) = 6.



Returns `6`, which correctly maps to the subarray `[2, 3]`. The logic successfully bounded the negative propagation and correctly reset the maximum when `4` proved to be better on its own than `-8` (`-2 * 4`).