## question

You are given an integer array coins representing coins of different denominations (e.g. 1 dollar, 5 dollars, etc) and an integer amount representing a target amount of money.
Return the fewest number of coins that you need to make up the exact target amount. If it is impossible to make up the amount, return -1.
You may assume that you have an unlimited number of each coin.

### 1. Restate

Given an array of coin denominations and a target amount. Find minimum coins required to sum to target. Infinite supply of each coin. Return -1 if impossible.

### 2. Clarifying Questions & I/O

* **Inputs:** `coins` (array of positive integers), `amount` (integer >= 0).
* **Output:** `int` (minimum coins, or -1).
* **Assumptions:** Coins aren't necessarily sorted. Can be empty? Assume valid array.
* **Example I/O:** `coins = [1, 3, 4], amount = 6` -> Output: `2` (3+3).

### 3. Hand-Trace (Input to Output)

Input: `coins = [1, 3, 4], amount = 6`
Try greedily: 4, then 1, 1. Total = 3 coins. Wait, 3+3 = 2 coins. Greedy fails.
Must evaluate all paths. Let's build bottom-up (sub-amount to target):

* 0 cents: 0 coins
* 1 cent: 1 coin (1)
* 2 cents: 2 coins (1+1)
* 3 cents: min(2cents + 1coin, 0cents + 3coin) -> min(3, 1) = 1
* 4 cents: min(3c+1c, 1c+3c, 0c+4c) -> min(2, 2, 1) = 1
* 5 cents: min(4c+1c, 2c+3c, 1c+4c) -> min(2, 2, 2) = 2
* 6 cents: min(5c+1c, 3c+3c, 2c+4c) -> min(3, 1+1, 2+1) = 2.
Output: 2.

### 4. Brainstorming & Complexity

* **Greedy:** Take largest possible coin. Fails on sets like `[1,3,4]`. Time: $O(n \log n)$.
* **DFS/Recursion (Brute Force):** Try every combination. Time: $O(S^n)$ where S is amount, n is num coins. Time Limit Exceeded.
* **DFS + Memoization (Top-Down DP):** Cache results for sub-amounts. Time: $O(S \times n)$, Space: $O(S)$ for recursion stack + cache.
* **Bottom-Up Dynamic Programming (from Step 3):** Iterate 1 to amount. Build DP array. Time: $O(S \times n)$, Space: $O(S)$. Safe from recursion depth limits.

### 5. Suggested Solutions

1. **Top-Down Memoization:** Start at amount, subtract coins recursively.
2. **Bottom-Up DP (The Hand-Trace Method):** Start at 0, build up to amount. Prefer this. Simple, iterative, avoids stack overflow, easy to reason about state transitions.

### 6. Outline (Bottom-Up DP)

```python
def coinChange(coins, amount):
    """
    Reframe: Shortest path to reach 'amount' using 'coins' as step sizes.
    State: 1D array DP tracking min coins for every sub-amount 0 to target. Chosen because problem has optimal substructure (min coins for X relies on min coins for X-coin).
    Invariant: dp[a] holds absolute min coins to make amount 'a'.

    min_coins_for(sub_amount) = look up previously computed minimum coins in DP table.

    Core logic:
    - initialize DP table for all amounts up to target with infinity.
    - base case: 0 coins needed for amount 0.
    - iterate through every sub-amount from 1 up to target.
    - for each sub-amount, try every coin denomination.
    - if the coin fits, calculate total coins: 1 + min_coins_for(sub_amount minus coin).
    - keep the minimum of these calculations.
    
    Edge cases:
    - amount is 0.
    - impossible to make exact change (return -1).
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton & Stubs**

```python
def coinChange(coins, amount):
    # Setup DP table
    dp_table = create_dp_table(amount)
    
    # Base case
    set_base_case(dp_table)
    
    # Core logic
    for sub_amount in range(1, amount + 1):
        for coin in coins:
            if coin_fits(sub_amount, coin):
                # calc: 1 + min_coins_for(sub_amount - coin)
                update_min_coins(dp_table, sub_amount, coin)
                
    return get_final_answer(dp_table, amount)

```

**Iteration 2: Fleshing out Core Logic (Replacing stubs)**

```python
def coinChange(coins, amount):
    # Setup DP table: use infinity to represent "impossible" initially
    dp = [float('inf')] * (amount + 1)
    
    # Base case
    dp[0] = 0
    
    # Core logic
    for i in range(1, amount + 1):
        for c in coins:
            # if coin fits
            if i - c >= 0:
                # 1 + min_coins_for(sub_amount - coin)
                dp[i] = min(dp[i], 1 + dp[i - c])
                
    # get_final_answer (leaving edge case patching for next step)
    return dp[amount]

```

**Iteration 3: Patching Edge Cases**

* *Edge case 1: Amount is 0.* If `amount=0`, loop doesn't run, `dp[0]` returns `0`. Correct.
* *Edge case 2: Impossible to make change.* If target is unreachable, `dp[amount]` remains `float('inf')`. Needs to return `-1`.

```python
def coinChange(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for c in coins:
            if i - c >= 0:
                dp[i] = min(dp[i], 1 + dp[i - c])
                
    # PATCH: Check for infinity to handle impossible cases
    return dp[amount] if dp[amount] != float('inf') else -1

```

### 8. Complexity & Optimization

* **Time Complexity:** $O(S \times n)$ where S is `amount` and n is `len(coins)`. Two nested loops.
* **Space Complexity:** $O(S)$ to store the DP array.
* **Optimization/Real-world Note:** The time and space complexities here are strictly optimal for the general exact-change problem. To marginally speed up execution in languages like Python, you can sort the `coins` array once at the beginning, then break out of the inner loop early if `i - c < 0`. This doesn't change Big-O but prunes dead branches.

```python
# Optional small pruning optimization
def coinChange(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    coins.sort() # Sort once to allow breaking early
    
    for i in range(1, amount + 1):
        for c in coins:
            if i - c < 0:
                break # Prune: larger coins won't fit either
            dp[i] = min(dp[i], 1 + dp[i - c])
            
    return dp[amount] if dp[amount] != float('inf') else -1

```