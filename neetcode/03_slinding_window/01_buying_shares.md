### question
You are given an integer array `prices` where `prices[i]` is the price of NeetCoin on the `ith` day.
You may choose a single day to buy one NeetCoin and choose a different day in the future to sell it.
Return the maximum profit you can achieve. You may choose to not make any transactions, in which case the profit would be `0`.

### 1. Restating the Question

Find max difference between two numbers in array where smaller number comes before larger number. Return 0 if no positive difference exists.

### 2. Clarifying Questions & Confirmations

* **Input:** Array of integers (`prices`). Non-negative? (Assume yes). Empty array possible? (Assume length >= 1).
* **Output:** Integer (max profit).
* **Constraint:** Buy day strictly before sell day. Can choose not to trade (profit 0).

### 3. Hand Execution

Input: `prices = [7, 1, 5, 3, 6, 4]`

* Start Day 1: price 7. No profit. Lowest so far: 7.
* Day 2: price 1. Lower than 7. Lowest so far: 1.
* Day 3: price 5. Sell today? Profit = 5 - 1 = 4. Max profit: 4.
* Day 4: price 3. Sell today? Profit = 3 - 1 = 2. Max profit remains 4.
* Day 5: price 6. Sell today? Profit = 6 - 1 = 5. Max profit: 5.
* Day 6: price 4. Sell today? Profit = 4 - 1 = 3. Max profit remains 5.
* Output: 5.

### 4. Brainstorming & Complexity

* **Approach 1:** Brute force. Check every possible buy and sell pair using nested loops. Time: $O(n^2)$. Space: $O(1)$. Expensive for large arrays.
* **Approach 2:** One-pass tracker. As we move right, we only care about the lowest price seen *so far* to maximize profit for the current day. Track lowest price. Track max profit. Time: $O(n)$. Space: $O(1)$.

### 5. Suggested Solutions

* **Brute Force:** Compare every day with every future day.
* **One-pass Min Tracker (Selected):** The hand-execution method. Simple, readable, straight-forward state tracking.

### 6. Outline

```python
def maxProfit(prices): 
    """
    Reframe: Maximize current value minus minimum previous value.
    State: lowest_price_seen (tracks minimum), best_profit (tracks max delta), chosen because 
           best sell requires lowest past buy.
    Invariant: lowest_price_seen is the strict minimum of all elements evaluated before the current element.

    helper_profit(current, lowest) = subtracts lowest from current.

    Core logic:
    - walk through each price in the timeline
    - update lowest price seen so far
    - calculate potential profit using current price and lowest price
    - update best profit if potential profit is higher
    - return best profit

    Edge cases:
    - timeline is empty or has only one day (no transactions possible)
    - prices strictly decreasing (no profit possible, returns 0)
    """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton with stubs**

```python
def maxProfit(prices):
    # TODO: init state variables
    
    # walk through each price
    for current_price in prices:
        # TODO: update lowest price seen
        # TODO: calc potential profit
        # TODO: update best profit
        pass
        
    # TODO: return best profit
    return 0

```

**Iteration 2: Core logic (Happy Path)**

```python
def maxProfit(prices):
    # init state variables
    lowest_price_seen = float('inf') # changed: handle any high first price
    best_profit = 0                  # changed: default is 0 per requirements
    
    # walk through each price
    for current_price in prices:
        # update lowest price seen
        lowest_price_seen = min(lowest_price_seen, current_price) # changed: track minimum
        
        # calc potential profit
        potential_profit = current_price - lowest_price_seen      # changed: calculate delta
        
        # update best profit
        best_profit = max(best_profit, potential_profit)          # changed: track maximum delta
        
    return best_profit

```

**Iteration 3: Edge cases added**

```python
def maxProfit(prices):
    # edge case: timeline too short to buy AND sell
    if not prices or len(prices) < 2: # added: short-circuit invalid input
        return 0
        
    lowest_price_seen = float('inf')
    best_profit = 0
    
    for current_price in prices:
        lowest_price_seen = min(lowest_price_seen, current_price)
        potential_profit = current_price - lowest_price_seen
        best_profit = max(best_profit, potential_profit)
        
    # strictly decreasing prices naturally result in best_profit remaining 0
    return best_profit

```

### 8. Complexity & Optimizations

* **Time Complexity:** $O(n)$ where $n$ is length of `prices`. Loop runs exactly once. `min` and `max` operations are $O(1)$. Extremely efficient.
* **Space Complexity:** $O(1)$. Only storing two integer variables (`lowest_price_seen`, `best_profit`) regardless of array size.
* **Optimizations:** Solution is mathematically optimal for single transaction. No heavy array slicing or extra memory overhead used. Code is clean and production-ready.