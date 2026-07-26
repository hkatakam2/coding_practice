### 1. Restate the problem

We are given an array of integers representing the amount of money in a line of houses. We need to find the maximum total amount of money we can collect. The only constraint is that we cannot collect money from two houses that are immediately next to each other.

In abstract terms, we must find the maximum sum of a subsequence where no two selected elements are adjacent in the original array. We are returning an integer representing this maximum sum, and we do not need to modify the input array.

### 2. Ask clarifying questions

Before writing code, I would confirm a few details with the interviewer:

* **Input size:** Can the array be empty? (Assumption: Yes, in which case the max money is 0).
* **Negative values:** Can a house have a negative amount or debt? (Assumption: No, houses have $\ge 0$ money. If they did have negative values, we would simply choose not to rob them, treating them as 0).
* **Integer overflow:** Can the total accumulated money exceed the maximum value of a 32-bit signed `int`? (Assumption: The total sum fits within a standard `int`. If the array is very large with large values, we would return a `long`).
* **Multiple valid answers:** We only need to return the maximum *amount*, not the specific indices of the houses we chose.

### 3. Work through an example by hand

Let's trace the input `nums = [2, 7, 9, 3, 1]`.

* **House 0 (2):** If we only look at the first house, the best we can do is rob it. Max: 2.
* **House 1 (7):** With two houses `[2, 7]`, we can rob the first or the second, but not both. Max: `max(2, 7) = 7`.
* **House 2 (9):** With `[2, 7, 9]`, we can either:
* Keep our max from before House 2 (which is 7).
* Rob House 2 (9) plus the max from *before* the previous house (which is 2). $9 + 2 = 11$.
* Max: `max(7, 11) = 11`.


* **House 3 (3):** With `[2, 7, 9, 3]`:
* Keep previous max: 11.
* Rob House 3 (3) + max from before previous (7). $3 + 7 = 10$.
* Max: `max(11, 10) = 11`.


* **House 4 (1):** With `[2, 7, 9, 3, 1]`:
* Keep previous max: 11.
* Rob House 4 (1) + max from before previous (11). $1 + 11 = 12$.
* Max: `max(11, 12) = 12`.



Final result: 12 (robbing houses 0, 2, and 4: $2 + 9 + 1 = 12$).

### 4. Brainstorm solutions aloud

* **Brute Force (Recursion):** We can explore every valid combination of houses. For each house, we either rob it (and skip the next) or skip it (and move to the next). This forms a decision tree. While correct, it overlaps subproblems heavily, leading to $O(2^n)$ time complexity.
* **Dynamic Programming (1D Array):** We can cache the results of our subproblems. As seen in the manual example, the maximum money at house `i` relies only on the maximums at `i-1` and `i-2`. We can maintain an array `dp` where `dp[i]` is the max money up to house `i`. Time complexity is $O(n)$, and space complexity is $O(n)$ for the array.
* **Space-Optimized Dynamic Programming:** Notice that to calculate the state for house `i`, we *only* ever look at `i-1` and `i-2`. The rest of the history in the `dp` array is never used again. We can replace the $O(n)$ array with just two integer variables tracking the "previous" and "two steps back" maximums. Time complexity remains $O(n)$, but space complexity drops to $O(1)$.

### 5. Select the solution

I will use the **Space-Optimized Dynamic Programming** approach. It is optimal in both time and space, conceptually straightforward to explain, and avoids the unnecessary allocation of an array.

### 6. Write the implementation outline

```java
int rob(int[] nums) {
    /*
     * Reframe:
     * Scan the houses and maintain the best possible haul up to the current 
     * house by deciding whether robbing the current house yields more money 
     * than skipping it.
     *
     * State:
     * Two integer variables: `prevTwo` (max money up to two houses ago) 
     * and `prevOne` (max money up to the previous house).
     * Chosen because the recursive relation only depends on the last two states, 
     * eliminating the need for an O(n) array.
     *
     * Invariant:
     * After processing index i, `prevOne` contains the maximum money that can 
     * be robbed from houses 0 through i, and `prevTwo` contains the maximum 
     * money from houses 0 through i-1.
     *
     * Core logic:
     * - handle edge cases (null or empty array)
     * - initialize our two tracking variables to 0
     * - loop through each house's money in the array
     * - calculate the max if we rob the current house (money + prevTwo)
     * - calculate the max if we skip the current house (prevOne)
     * - the new maximum for the current position is the larger of the two
     * - shift the tracking variables forward for the next iteration
     * - return the most recent maximum (prevOne)
     *
     * Edge cases:
     * - empty input
     * - input with only one house
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton and state setup**

```java
int rob(int[] nums) {
    if (nums == null || nums.length == 0) {
        return 0;
    }

    // State to track the maximums from the last two steps
    int prevTwo = 0;
    int prevOne = 0;

    // TODO: loop through each house and update state
    
    return prevOne;
}

```

*Why this setup:* We handle the null/empty edge case immediately. Setting both `prevTwo` and `prevOne` to 0 perfectly handles the bounds before we start iterating through the array.

**Iteration 2: Core loop and recurrence relation**

```java
int rob(int[] nums) {
    if (nums == null || nums.length == 0) {
        return 0;
    }

    int prevTwo = 0;
    int prevOne = 0;

    for (int money : nums) {
        // Added: decide whether to rob the current house or skip it.
        // Robbing it means we add its money to the max from two houses ago.
        // Skipping it means we just keep the max from the previous house.
        int currentMax = Math.max(prevTwo + money, prevOne);

        // TODO: shift our tracking variables forward
    }
    
    return prevOne;
}

```

**Iteration 3: Complete the state transition**

```java
int rob(int[] nums) {
    if (nums == null || nums.length == 0) {
        return 0;
    }

    int prevTwo = 0;
    int prevOne = 0;

    for (int money : nums) {
        int currentMax = Math.max(prevTwo + money, prevOne);

        // Added: shift the window forward.
        // What was the previous house becomes two houses ago.
        prevTwo = prevOne;
        // The current best haul becomes the previous house for the next iteration.
        prevOne = currentMax;
    }
    
    return prevOne;
}

```

**Edge-case pass**
Let's review the edge cases identified in the outline:

* **Empty array / Null:** Handled by the explicit check at the top. Returns 0.
* **One element (`[5]`):**
* Loop starts. `money = 5`.
* `currentMax = max(0 + 5, 0) = 5`.
* `prevTwo = 0`, `prevOne = 5`.
* Loop ends. Returns `prevOne` (5). Correct.


* **Integer overflow:** If the constraint was that `nums` could sum to greater than `Integer.MAX_VALUE`, we'd change `prevTwo`, `prevOne`, and `currentMax` to `long`. For standard LeetCode/interview constraints, `int` is sufficient.

The logic holds up perfectly. No additional patches are required.

### 8. Analyze expensive sections and optimize

Because we already went straight to the optimized DP approach, the complexity is minimal.

* **Time Complexity:** $O(n)$ where $n$ is the length of `nums`. We scan the array exactly once, performing $O(1)$ operations per element.
* **Space Complexity:** $O(1)$. We only maintain a few integer variables (`prevTwo`, `prevOne`, `currentMax`, `money`), allocating no auxiliary data structures.

### Final Code

```java
class Solution {
    public int rob(int[] nums) {
        if (nums == null || nums.length == 0) {
            return 0;
        }

        int prevTwo = 0;
        int prevOne = 0;

        for (int money : nums) {
            int currentMax = Math.max(prevTwo + money, prevOne);
            
            prevTwo = prevOne;
            prevOne = currentMax;
        }
        
        return prevOne;
    }
}

```

### Brief test walkthrough

Let's test it with `nums = [2, 1, 1, 2]`. This is an interesting case because the optimal choice is the first and last element, skipping two in the middle.

1. **Initialize:** `prevTwo = 0`, `prevOne = 0`
2. **Iterate money = 2:**
* `currentMax = max(0 + 2, 0) = 2`
* `prevTwo = 0`, `prevOne = 2`


3. **Iterate money = 1:**
* `currentMax = max(0 + 1, 2) = 2`
* `prevTwo = 2`, `prevOne = 2`


4. **Iterate money = 1:**
* `currentMax = max(2 + 1, 2) = 3`
* `prevTwo = 2`, `prevOne = 3`


5. **Iterate money = 2:**
* `currentMax = max(2 + 2, 3) = 4`
* `prevTwo = 3`, `prevOne = 4`


6. **End loop.** Return `prevOne` (4).

The result is `4`, which correctly matches robbing index 0 (value 2) and index 3 (value 2). The code is correct and handles gaps greater than one house seamlessly.