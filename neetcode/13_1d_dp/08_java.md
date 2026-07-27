### 1. Restate the problem

We are given a collection of coin denominations and a target monetary amount. We need to find the absolute minimum number of coins required to sum up to exactly that target amount. We can use as many of each coin denomination as we need. If no combination of the provided coins can exactly match the target, we must return `-1`.

### 2. Ask clarifying questions

Before writing code, I would confirm a few assumptions about the input:

* **Can the target amount be `0`?** (Assuming yes, the answer should be `0` coins).
* **Can the target amount be negative?** (Assuming no, or if so, return `-1`).
* **Are all coin denominations strictly positive integers?** (Assuming yes; a `0` or negative coin would complicate the logic or cause infinite loops).
* **Is the `coins` array sorted?** (Assuming no, we shouldn't rely on order).
* **What is the maximum target amount?** (Assuming it fits well within standard memory constraints, e.g., $\le 10^4$, so an array of this size is perfectly fine).

### 3. Work through an example by hand

Let's use an example that defeats a simple "greedy" approach (picking the largest coin first).
`coins = [1, 3, 4]`, `amount = 6`

If we used a greedy approach:

* Take `4`. Remaining: `2`.
* Take `1`. Remaining: `1`.
* Take `1`. Remaining: `0`.
Total: `3` coins.

But we can see by looking at it that `3 + 3 = 6`, which uses only `2` coins.

To systematically find the optimal `2` coins, we can build the answer from the bottom up. What is the minimum coins for `amount = 1`? `amount = 2`?

* Target `0`: `0` coins
* Target `1`: Need coin `1` $\to$ `1` coin
* Target `2`: Need coin `1` $\to$ `1` + (Target `1` coins) $\to$ `2` coins
* Target `3`: Need coin `3` $\to$ `1` coin
* Target `4`: Need coin `4` $\to$ `1` coin
* Target `5`: Need coin `4` $\to$ `1` + (Target `1` coins) $\to$ `2` coins
* Target `6`:
* Using coin `1`: `1` + (Target `5` coins: `2`) = `3`
* Using coin `3`: `1` + (Target `3` coins: `1`) = `2`  *(Best)*
* Using coin `4`: `1` + (Target `2` coins: `2`) = `3`



The minimum for `6` is `2` coins.

### 4. Brainstorm solutions aloud

**Approach 1: Recursion (Brute Force)**
We could try every possible combination of coins using recursion. For the current amount, branch out by subtracting each available coin and recursing.

* *Time complexity:* $O(S^n)$ where $S$ is the amount and $n$ is the number of coins.
* *Verdict:* Way too slow. It recomputes the same subproblems repeatedly.

**Approach 2: Breadth-First Search (BFS)**
We can think of this as an unweighted shortest-path problem. Start at node `0` and add edges for each coin denomination. The first time we reach the node representing `amount`, the depth of the BFS is our answer.

* *Time complexity:* $O(S \times n)$
* *Verdict:* Very efficient and logically sound, but requires managing a queue and a visited set.

**Approach 3: Bottom-Up Dynamic Programming (Tabulation)**
As demonstrated in the manual example, we can maintain an array `dp` of size `amount + 1` where `dp[i]` represents the minimum coins needed for amount `i`. For each amount from `1` to `amount`, we look back at `dp[i - coin]` for all valid coins.

* *Time complexity:* $O(S \times n)$
* *Space complexity:* $O(S)$
* *Verdict:* Optimal. The array lookup is extremely fast, has minimal memory overhead, and avoids the queue management of BFS.

### 5. Select the solution

I will go with **Bottom-Up Dynamic Programming**. It safely fulfills constraints, is standard for this class of unbounded knapsack problems, and relies on a simple, flat array rather than complex data structures.

### 6. Write the implementation outline

```java
int coinChange(int[] coins, int amount) {
    /*
     * Reframe:
     * Build up the minimum coins needed for every amount from 0 to the target.
     *
     * State:
     * An integer array 'dp' of size amount + 1.
     * Chosen because we need fast, indexed access to previous optimal subproblems.
     *
     * Invariant:
     * dp[i] always holds the minimum number of coins to make amount i. 
     * If dp[i] is greater than the target amount, it is unreachable.
     *
     * Core logic:
     * - create the dp array and fill it with a placeholder "infinity" value
     * - set dp[0] to 0, since 0 coins are needed for amount 0
     * - for each amount from 1 up to the target amount:
     *   - check every coin denomination
     *   - if the coin can fit in the current amount:
     *     - update the current amount's dp value with the minimum of its 
     *       existing value or 1 + the dp value of the remainder
     * - return the dp value for the target amount, or -1 if still "infinity"
     *
     * Edge cases:
     * - target amount is 0
     * - coins array is empty
     * - no combination of coins can form the amount
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton**
First, we'll establish the basic state array and bounds checking. We fill the array with a safe "maximum" value. We use `amount + 1` instead of `Integer.MAX_VALUE` to avoid integer overflow later when we add `1` to the remainder.

```java
public int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    
    // Fill with a safe "infinity" value that won't overflow when we add 1
    int maxPlaceholder = amount + 1; 
    Arrays.fill(dp, maxPlaceholder);
    dp[0] = 0; // Base case

    // TODO: loop through all amounts
    // TODO: loop through all coins for each amount
    
    return dp[amount] == maxPlaceholder ? -1 : dp[amount];
}

```

**Iteration 2: Implement the core loop**
Next, we add the iterative loops to build up our `dp` array.

```java
public int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    int maxPlaceholder = amount + 1; 
    Arrays.fill(dp, maxPlaceholder);
    dp[0] = 0;

    // Added: Iterate through every amount up to the target
    for (int currentAmount = 1; currentAmount <= amount; currentAmount++) {
        // Added: Try every coin for the current amount
        for (int coin : coins) {
            // TODO: verify the coin fits and update the dp array
        }
    }
    
    return dp[amount] == maxPlaceholder ? -1 : dp[amount];
}

```

**Iteration 3: Complete the happy path**
Now, we apply the dynamic programming recurrence relation inside the innermost loop.

```java
public int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    int maxPlaceholder = amount + 1; 
    Arrays.fill(dp, maxPlaceholder);
    dp[0] = 0;

    for (int currentAmount = 1; currentAmount <= amount; currentAmount++) {
        for (int coin : coins) {
            // Added: Only consider the coin if it doesn't exceed our current target
            if (coin <= currentAmount) {
                int remainder = currentAmount - coin;
                // Added: Take the minimum of keeping the current state or using this coin
                dp[currentAmount] = Math.min(dp[currentAmount], dp[remainder] + 1);
            }
        }
    }
    
    return dp[amount] == maxPlaceholder ? -1 : dp[amount];
}

```

**Edge-case pass**
Let's review the edge cases identified in the outline:

* *Target amount is `0`:* The loops `currentAmount = 1; currentAmount <= 0` will skip entirely. `dp[0]` is `0`. Returns `0`. Works perfectly.
* *Unreachable amount:* If `amount = 3` and `coins = [2]`, `dp[1]` stays `4`, `dp[2]` becomes `1`, `dp[3]` stays `4`. Returns `-1`. Works perfectly.
* *Integer overflow:* Because we used `amount + 1` instead of `Integer.MAX_VALUE`, `dp[remainder] + 1` will max out at `amount + 2`, remaining well within safe integer bounds.

The code is robust and requires no specific patch logic for these scenarios.

### Final code

```java
import java.util.Arrays;

class Solution {
    public int coinChange(int[] coins, int amount) {
        if (amount == 0) {
            return 0;
        }
        
        int[] dp = new int[amount + 1];
        int maxPlaceholder = amount + 1; 
        
        Arrays.fill(dp, maxPlaceholder);
        dp[0] = 0;

        for (int currentAmount = 1; currentAmount <= amount; currentAmount++) {
            for (int coin : coins) {
                if (coin <= currentAmount) {
                    int remainder = currentAmount - coin;
                    dp[currentAmount] = Math.min(dp[currentAmount], dp[remainder] + 1);
                }
            }
        }
        
        return dp[amount] == maxPlaceholder ? -1 : dp[amount];
    }
}

```

### Complexity

* **Time Complexity:** $O(S \times n)$, where $S$ is the `amount` and $n$ is the length of the `coins` array. We iterate up to `amount`, and for each step, we iterate through every coin.
* **Space Complexity:** $O(S)$ to maintain the `dp` array of size `amount + 1`.

### Brief test walkthrough

Let's test it with `coins = [1, 3, 4]` and `amount = 6`.

1. `dp` initialized to `[0, 7, 7, 7, 7, 7, 7]` (size 7, maxPlaceholder is 7).
2. `currentAmount = 1`: Coin 1 fits. `dp[1] = min(7, dp[0] + 1) = 1`.
3. `currentAmount = 2`: Coin 1 fits. `dp[2] = min(7, dp[1] + 1) = 2`.
4. `currentAmount = 3`:
* Coin 1 fits. `dp[3] = min(7, dp[2] + 1) = 3`.
* Coin 3 fits. `dp[3] = min(3, dp[0] + 1) = 1`.


5. `currentAmount = 4`:
* Coin 1 fits $\to$ `dp[4] = 2`
* Coin 3 fits $\to$ `dp[4] = min(2, dp[1] + 1) = 2`
* Coin 4 fits $\to$ `dp[4] = min(2, dp[0] + 1) = 1`


6. `currentAmount = 5`:
* Coin 1 $\to$ `dp[5] = 2`
* Coin 3 $\to$ `dp[5] = min(2, dp[2] + 1) = 2`
* Coin 4 $\to$ `dp[5] = min(2, dp[1] + 1) = 2`


7. `currentAmount = 6`:
* Coin 1 $\to$ `dp[6] = min(7, dp[5] + 1) = 3`
* Coin 3 $\to$ `dp[6] = min(3, dp[3] + 1) = 2`
* Coin 4 $\to$ `dp[6] = min(2, dp[2] + 1) = 2`


8. Loop finishes. `dp[6]` is `2`. We return `2`.

The logic holds and cleanly returns the optimal answer.