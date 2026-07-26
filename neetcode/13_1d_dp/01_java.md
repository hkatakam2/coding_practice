### 1. Restate the problem

We need to calculate the total number of unique sequences of 1-step and 2-step climbs that sum up to exactly `n` steps.

* **Given:** An integer `n`, representing the total number of steps in the staircase.
* **Must return:** The count of distinct ways to reach the exact top.
* **Main constraint:** At any given point, we can only advance by exactly 1 step or exactly 2 steps. The order of these steps matters (e.g., a 1-step then 2-step is distinct from a 2-step then 1-step).

### 2. Ask clarifying questions

Before writing code, I would clarify the following with the interviewer:

* **Input size:** What is the maximum value of `n`? If `n` is greater than 45, the number of ways will exceed `Integer.MAX_VALUE` (2,147,483,647), and we would need to return a `long`.
* **Zero or negative input:** Can `n` be 0 or negative?
* **Valid domain:** For this problem, I will assume `n >= 1`. I'll also assume `n <= 45` so that the result safely fits within a standard 32-bit signed `int`.

### 3. Work through an example by hand

Let's use a representative example: `n = 4`.

We build up to the answer by looking at the smaller steps.

* **n = 1:** Only 1 way to reach step 1 (take one 1-step). -> `[1]`
* **n = 2:** 2 ways to reach step 2. -> `[1, 1]`, `[2]`
* **n = 3:** To reach step 3, we can either:
* Step up 1 from step 2: `[1, 1, +1]`, `[2, +1]`
* Step up 2 from step 1: `[1, +2]`
* Total ways for step 3 = ways(2) + ways(1) = 2 + 1 = 3.


* **n = 4:** To reach step 4, we can either:
* Step up 1 from step 3: `[1, 1, 1, +1]`, `[2, 1, +1]`, `[1, 2, +1]`
* Step up 2 from step 2: `[1, 1, +2]`, `[2, +2]`
* Total ways for step 4 = ways(3) + ways(2) = 3 + 2 = 5.



The final output for `n = 4` is `5`.

### 4. Brainstorm solutions aloud

* **Direct Recursion (Brute Force):** We can simulate the process directly by expressing it as `climbStairs(n) = climbStairs(n - 1) + climbStairs(n - 2)`. This creates a massive branching tree of possibilities. While easy to write, it repeats identical calculations. Time complexity is $O(2^n)$, space complexity is $O(n)$ for the recursion stack.
* **Top-Down Memoization:** We can use the brute-force recursion but store the answers in a `HashMap` or array as we compute them. If we encounter a step we've already solved, we return the cached value. Time complexity drops to $O(n)$ and space complexity is $O(n)$.
* **Bottom-Up Dynamic Programming (Array):** We can build the answers iteratively from step 1 up to step `n`, storing each result in an array `dp[]` where `dp[i] = dp[i-1] + dp[i-2]`. Time complexity is $O(n)$, space complexity is $O(n)$.
* **Space-Optimized Bottom-Up DP:** Looking at the array solution, to calculate step `i`, we only ever need the results of `i-1` and `i-2`. The rest of the array is dead memory. We can replace the array with two integer variables that track just the previous two steps. Time complexity is $O(n)$, space complexity is $O(1)$.

### 5. Select the solution

I will select the **Space-Optimized Bottom-Up DP**.

It provides optimal $O(n)$ time complexity and $O(1)$ space complexity. It is straightforward to explain, avoids the allocation of an array, and entirely bypasses the risk of `StackOverflowError` associated with deep recursion.

### 6. Write the implementation outline

```java
int climbStairs(int n) {
    /*
     * Reframe:
     * The number of ways to reach step N is exactly the number of ways 
     * to reach step N-1 plus the number of ways to reach step N-2. 
     *
     * State:
     * We need two variables to track the number of ways to reach 
     * the two most recent steps.
     * Chosen because we only ever look back exactly two steps, making
     * an entire array or map unnecessary.
     *
     * Invariant:
     * At the start of iteration `i`, `twoStepsBefore` holds the ways to reach `i-2`,
     * and `oneStepBefore` holds the ways to reach `i-1`.
     *
     * Core logic:
     * - Handle base cases where n is 1 or 2 directly.
     * - Initialize our two state variables for steps 1 and 2.
     * - Iterate from step 3 up to n.
     * - In each iteration, calculate the current step's ways by summing the two previous ones.
     * - Shift the state variables forward: what was "one step before" becomes "two steps before",
     *   and what was "current" becomes "one step before".
     * - Return the calculated current ways.
     *
     * Edge cases:
     * - n = 1
     * - n = 2
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton and base cases**
First, let's establish the signature and handle the immediate base cases where the pattern hasn't built up enough history to require a loop.

```java
int climbStairs(int n) {
    // Base cases: if the staircase is only 1 or 2 steps, 
    // the answer perfectly matches n.
    if (n <= 2) {
        return n;
    }

    // TODO: initialize state variables for looking back
    // TODO: iterate from step 3 up to n
    
    return 0; // placeholder
}

```

**Iteration 2: Adding state and the loop**
Now we establish the two variables we need to maintain our sliding window of history, and set up the loop.

```java
int climbStairs(int n) {
    if (n <= 2) {
        return n;
    }

    // Added: state variables initialized to represent steps 1 and 2.
    int twoStepsBefore = 1;
    int oneStepBefore = 2;
    int currentWays = 0;

    // Added: loop from 3 to n.
    for (int currentStep = 3; currentStep <= n; currentStep++) {
        // TODO: calculate currentWays
        // TODO: slide the variables forward
    }
    
    return currentWays;
}

```

**Iteration 3: Completing the core logic**
Inside the loop, we implement the invariant transition: sum the past two records, and shift the window forward.

```java
int climbStairs(int n) {
    if (n <= 2) {
        return n;
    }

    int twoStepsBefore = 1;
    int oneStepBefore = 2;
    int currentWays = 0;

    for (int currentStep = 3; currentStep <= n; currentStep++) {
        // Added: calculation and sliding window transition
        currentWays = oneStepBefore + twoStepsBefore;
        
        // Shift history forward for the next iteration
        twoStepsBefore = oneStepBefore;
        oneStepBefore = currentWays;
    }
    
    return currentWays;
}

```

### 8. Edge-case walkthrough and patches

* **n = 1:** The `if (n <= 2)` block catches this immediately and returns `1`. Correct.
* **n = 2:** The `if (n <= 2)` block catches this immediately and returns `2`. Correct.
* **Integer Overflow:** If `n` is large (e.g., `n = 50`), `currentWays` will exceed the maximum value of a 32-bit signed integer. The constraints normally state `1 <= n <= 45` for this problem on platforms like LeetCode, so an `int` perfectly suffices without rolling over into negatives. If `n` could be larger, we would simply change our variables to `long`. No code patch is required under standard constraints.

### 9. Final code

Here is the clean, final version of the code.

```java
public int climbStairs(int n) {
    if (n <= 2) {
        return n;
    }

    int twoStepsBefore = 1;
    int oneStepBefore = 2;
    int currentWays = 0;

    for (int currentStep = 3; currentStep <= n; currentStep++) {
        currentWays = oneStepBefore + twoStepsBefore;
        twoStepsBefore = oneStepBefore;
        oneStepBefore = currentWays;
    }
    
    return currentWays;
}

```

### 10. Complexity

* **Time Complexity:** $O(n)$
The algorithm loops from `3` to `n`. Inside the loop, we perform a few basic arithmetic operations and assignments. This requires $n - 2$ iterations, which simplifies to $O(n)$ linear time.
* **Space Complexity:** $O(1)$
We are only tracking three integer variables (`twoStepsBefore`, `oneStepBefore`, `currentWays`) regardless of how large `n` gets. Space remains strictly constant.

### 11. Brief test walkthrough

Let's do a quick dry run with **`n = 4`**:

1. `n` is 4, which bypasses the `n <= 2` base case check.
2. Initialization: `twoStepsBefore = 1`, `oneStepBefore = 2`.
3. Loop `currentStep = 3`:
* `currentWays = 2 + 1 = 3`.
* Update state: `twoStepsBefore = 2`, `oneStepBefore = 3`.


4. Loop `currentStep = 4`:
* `currentWays = 3 + 2 = 5`.
* Update state: `twoStepsBefore = 3`, `oneStepBefore = 5`.


5. Loop terminates (`currentStep` becomes 5, violating `currentStep <= 4`).
6. Method returns `currentWays`, which is `5`.

This exactly matches our manual evaluation.