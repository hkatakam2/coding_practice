### 1. Restate the problem

We are given an array of stock prices where each element represents the price of NeetCoin on a specific day. We need to find the maximum possible profit we can make by performing exactly one buy transaction and exactly one sell transaction. The sell day must be strictly after the buy day. If it's impossible to make a profit (for example, if prices continually decrease), we should return 0.

### 2. Ask clarifying questions

Before writing the code, I would clarify a few details to ensure my assumptions are correct:

* **Input size:** How large can the `prices` array be? (I'll assume it can be up to $10^5$ elements, meaning an $O(n^2)$ solution will be too slow).
* **Null or empty input:** Can the input array be null or empty? (I will assume yes, and will return a profit of 0 in these cases).
* **Negative values:** Can stock prices be negative? (I will assume they are non-negative, though the logic would largely remain the same regardless).
* **Integer capacity:** Can the maximum profit exceed the maximum value of a 32-bit signed integer? (I will assume `int` is sufficient since stock prices usually fit well within this range).

### 3. Work through an example by hand

Let's trace a representative input: `prices = [7, 1, 5, 3, 6, 4]`.

* **Day 0 (Price: 7):** Best buy price so far is 7. No profit can be made yet. Max profit = 0.
* **Day 1 (Price: 1):** We can't sell for a profit (1 - 7 = -6). But we found a new lowest price: 1. Max profit remains 0.
* **Day 2 (Price: 5):** If we sell today using the lowest prior price (1), profit is 5 - 1 = 4. We update max profit to 4.
* **Day 3 (Price: 3):** Selling today yields 3 - 1 = 2. Max profit remains 4. Best buy is still 1.
* **Day 4 (Price: 6):** Selling today yields 6 - 1 = 5. We update max profit to 5.
* **Day 5 (Price: 4):** Selling today yields 4 - 1 = 3. Max profit remains 5.

The final max profit is 5.

### 4. Brainstorm solutions aloud

* **Direct Simulation (Brute Force):** The most direct approach is to compare every possible pair of days. We use a nested loop where the outer loop picks a buy day `i` and the inner loop picks a strictly future sell day `j`. We calculate `prices[j] - prices[i]` and track the maximum. This is easy to verify but costs $O(n^2)$ time. Given our assumed constraints, this will likely time out.
* **One Pass (Tracking the Minimum):** Thinking back to the manual example, I only ever needed to know one thing about the past: *What was the absolute lowest price I could have bought at before today?* As I iterate through the array, I can maintain a running minimum of the prices seen so far. At each step, I can check how much profit I'd make if I sold at the current price, using that running minimum as my buy price. This only requires a single pass through the array, giving us $O(n)$ time and $O(1)$ space.

### 5. Select the solution

I will use the **One Pass (Tracking the Minimum)** approach.
It is optimal, easy to explain, and trivial to implement without bugs. It avoids unnecessary space complexity and naturally handles edge cases like strictly decreasing prices.

### 6. Write the implementation outline

Here is the conceptual blueprint for the logic:

```java
int maxProfit(int[] prices) {
    /*
     * Reframe:
     * Find the maximum difference between a value and the smallest value that precedes it.
     *
     * State:
     * minimumPriceSeen: the lowest price encountered so far.
     * maxProfit: the largest profit recorded so far.
     * Chosen because tracking the minimum prior value is sufficient to know the best buy price.
     *
     * Invariant:
     * At the start of processing day i, minimumPriceSeen is the exact minimum of all prices from day 0 to i-1.
     *
     * Core logic:
     * - handle null or short input gracefully
     * - initialize maxProfit to 0
     * - initialize minimumPriceSeen to a very high number
     * - inspect each price in the array
     * - compute the potential profit if we sold at the current price
     * - update maxProfit if this potential profit is higher
     * - update minimumPriceSeen if the current price is strictly lower
     * - return maxProfit
     *
     * Edge cases:
     * - empty input or length 1 (no transaction possible)
     * - prices constantly decreasing (maxProfit should remain 0)
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton and state variables**
First, I will set up the method signature, the guard clauses, and the state variables required to track the minimum price and the maximum profit.

```java
public int maxProfit(int[] prices) {
    if (prices == null || prices.length < 2) {
        return 0;
    }

    int minimumPriceSeen = Integer.MAX_VALUE;
    int maxProfit = 0;

    // TODO: iterate over prices
    // TODO: update maxProfit and minimumPriceSeen

    return maxProfit;
}

```

**Iteration 2: Completing the core logic**
Next, I will translate the core iteration logic from the outline into code. I will use an enhanced `for` loop since I only need the values, not the indices.

```java
public int maxProfit(int[] prices) {
    if (prices == null || prices.length < 2) {
        return 0;
    }

    int minimumPriceSeen = Integer.MAX_VALUE;
    int maxProfit = 0;

    for (int currentPrice : prices) {
        // Added: Calculate the profit if we sell today.
        int potentialProfit = currentPrice - minimumPriceSeen;
        
        // Added: Update maxProfit if we found a better selling opportunity.
        if (potentialProfit > maxProfit) {
            maxProfit = potentialProfit;
        }

        // Added: Update the lowest price seen so far for future days.
        if (currentPrice < minimumPriceSeen) {
            minimumPriceSeen = currentPrice;
        }
    }

    return maxProfit;
}

```

**Edge-case pass**
Let's review the edge cases identified earlier:

1. **Empty input / Length 1:** The guard clause `prices == null || prices.length < 2` safely catches this and returns `0`.
2. **Prices constantly decreasing (e.g., `[7, 6, 4, 3, 1]`):**
* `minimumPriceSeen` gets updated down to 1.
* `potentialProfit` will always be negative.
* `maxProfit` remains exactly `0`, which is the correct requirement for not making any transaction. No patches are needed.



### 8. Analyze expensive sections and optimize

* **Time Complexity:** $O(n)$ where $n$ is the length of the `prices` array. We do exactly one pass over the elements, performing constant time $O(1)$ operations at each step.
* **Space Complexity:** $O(1)$. We are only storing a couple of primitive integer variables (`minimumPriceSeen` and `maxProfit`), requiring no auxiliary data structures.

Since we must evaluate every price at least once to ensure we don't miss a massive price spike, this $O(n)$ time complexity is the theoretical lower bound. No further optimizations are necessary.

### Final Code

```java
public int maxProfit(int[] prices) {
    if (prices == null || prices.length < 2) {
        return 0;
    }

    int minimumPriceSeen = Integer.MAX_VALUE;
    int maxProfit = 0;

    for (int currentPrice : prices) {
        int potentialProfit = currentPrice - minimumPriceSeen;
        
        if (potentialProfit > maxProfit) {
            maxProfit = potentialProfit;
        }

        if (currentPrice < minimumPriceSeen) {
            minimumPriceSeen = currentPrice;
        }
    }

    return maxProfit;
}

```

### Brief test walkthrough

* **Main example:** `[7, 1, 5, 3, 6, 4]`
* Skips 7 (profit negative, min set to 7).
* Hits 1 (min set to 1).
* Hits 5 (profit 4, max set to 4).
* Hits 6 (profit 5, max set to 5).
* Result: `5`. (Expected: 5).


* **Decreasing sequence:** `[7, 6, 4, 3, 1]`
* `potentialProfit` is always negative.
* `maxProfit` never updates from its initial `0`.
* Result: `0`. (Expected: 0).


* **Smallest valid input:** `[5, 10]`
* Hits 5 (min set to 5).
* Hits 10 (profit 5, max set to 5).
* Result: `5`. (Expected: 5).