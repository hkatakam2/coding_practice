## question
You are given an integer array `coins` representing coins of different denominations (e.g. 1 dollar, 5 dollars, etc) and an integer `amount` representing a target amount of money.
Return the number of distinct combinations that total up to `amount`. If it's impossible to make up the amount, return `0`.
You may assume that you have an unlimited number of each coin and that each value in `coins` is unique.

# 1. Restate

Given coin denominations (unlimited supply each) and a target `amount`, count how many **distinct combinations** sum to `amount`. Order doesn't matter — {1,1,2} and {2,1,1} are the same combination. Return 0 if impossible.

# 2. Clarifying questions

- Combinations not permutations? **Yes** — {1,2} == {2,1}, counted once.
- `amount == 0`? → 1 (the empty combination).
- Coins distinct, positive ints? Assume yes.
- Range? `amount` up to ~5000, coins length small — DP is fine.
- Count of combos, not the combos themselves? Yes, just the number.

# 3. Example by hand

`coins = [1,2,5]`, `amount = 5`

List distinct combos summing to 5:
- `5`
- `2+2+1`
- `2+1+1+1`
- `1+1+1+1+1`

→ **4**

(Note `2+2+1` and `1+2+2` count once — that's the key constraint.)

# 4. Brainstorm

The "order doesn't matter" rule is the whole difficulty. If we naively try every coin at every step, we'd count `1+2+2` and `2+1+2` separately → overcounts permutations.

Fix: impose an order. Process coins **one denomination at a time**. Decide "how many of coin A, then how many of coin B…" — never revisit an earlier coin. That forces a canonical ordering, so each combination counted once.

Options:
- **(a) Recursion + memo**: `count(i, remaining)` = ways using coins from index `i` onward. Branch: skip coin `i`, or use coin `i` (stay at `i`, reduce remaining). Time `O(coins × amount)`, space same for memo + recursion stack.
- **(b) Bottom-up DP, 1D array**: `dp[x]` = ways to make `x`. Loop **coins on the outside**, amounts inside. Outer-coin loop is what enforces no-permutation. Time `O(coins × amount)`, space `O(amount)`.
- **(c) Naive recursion no memo**: exponential, blows up.

(b) is the clean canonical answer and folds directly from the by-hand "one denomination at a time" insight. (a) reads slightly more naturally as plain logic.

# 5. Pick a solution

Both (a) and (b) are `O(coins × amount)`. (a) recursion+memo maps most directly to the plain-English "for this coin, how many do I take" reasoning; (b) is the tightest standard solution and is literally the by-hand "process one denomination at a time."

Which do you want to build?

- **A** — recursion + memo (reads most like the verbal logic)
- **B** — bottom-up 1D DP (canonical, tightest, = the by-hand insight)

# 6. Outline

```python
def change(amount, coins):  # -> int
    """
    Reframe: count combinations (not permutations) -> impose an order by
        deciding coin denominations one at a time, never going back to an
        earlier coin. That canonical ordering kills duplicate orderings.
    State: recursion over (i, remaining) where i = index into coins we are
        "allowed to still use from", remaining = amount left to make.
        Chosen because the only two real decisions at each coin are:
        how many of THIS coin (modeled as use-one-and-stay), or move on.
    Invariant: we only ever use coins at index >= i, so each combination is
        built in nondecreasing coin-index order -> counted exactly once.

    waysFrom(i, remaining) = number of combinations of coins[i:] summing to remaining.

    Core logic:
    - waysFrom(i, remaining):
        - if remaining filled exactly -> this is one valid combination, count it
        - otherwise two independent choices, add their counts:
            - skip coin i entirely, move to next coin
            - use one coin i, stay on coin i (unlimited supply)
    - answer = waysFrom(start, amount)

    Edge cases:
    - remaining becomes 0 -> success leaf (return 1)
    - ran out of coins but remaining still > 0 -> dead end (return 0)
    - using coin i would overshoot remaining -> that branch contributes 0
    - amount == 0 at top -> empty combination -> 1
    - repeated (i, remaining) states -> memoize to avoid recompute
    """
```

# 7. Iterative implementation

**Skeleton** — happy path, stubs for the decisions:

```python
def change(amount, coins):
    def waysFrom(i, remaining):
        if remaining == 0:
            return 1                      # filled exactly -> one combo
        # two choices, summed:
        skip = ...   # don't use coin i, advance
        take = ...   # use one coin i, stay
        return skip + take
    return waysFrom(0, amount)
```

**Iter 1** — fill the two branches:

```python
def change(amount, coins):
    def waysFrom(i, remaining):
        if remaining == 0:
            return 1
        skip = waysFrom(i + 1, remaining)         # move past coin i
        take = waysFrom(i, remaining - coins[i])  # use coin i, stay on it
        return skip + take
    return waysFrom(0, amount)
```

Core logic done — but `take` can go negative / `i` can run off the end. Now walk edges.

**Edge: ran out of coins, remaining > 0** → index `i` out of range. Add guard before touching `coins[i]`:

```python
def change(amount, coins):
    def waysFrom(i, remaining):
        if remaining == 0:
            return 1
        if i == len(coins):           # no coins left, didn't reach 0 -> dead end
            return 0
        skip = waysFrom(i + 1, remaining)
        take = waysFrom(i, remaining - coins[i])
        return skip + take
    return waysFrom(0, amount)
```

**Edge: taking coin i overshoots** (`remaining - coins[i] < 0`) → only take when it fits:

```python
def change(amount, coins):
    def waysFrom(i, remaining):
        if remaining == 0:
            return 1
        if i == len(coins):
            return 0
        skip = waysFrom(i + 1, remaining)
        take = 0
        if coins[i] <= remaining:                  # only take if it fits
            take = waysFrom(i, remaining - coins[i])
        return skip + take
    return waysFrom(0, amount)
```

**Edge: amount == 0** → handled free: top call `waysFrom(0,0)` hits `remaining==0` → 1. ✓
**Edge: impossible amount** → all branches dead-end to 0, sum is 0. ✓

# 8. Complexity + optimization

As written, `(i, remaining)` states recur many times → exponential blowup. The cheap fix is **memoization** on the unique state pair. There are at most `len(coins) × (amount+1)` distinct states, each computed once.

```python
from functools import cache

def change(amount, coins):
    @cache
    def waysFrom(i, remaining):
        if remaining == 0:
            return 1
        if i == len(coins):
            return 0
        skip = waysFrom(i + 1, remaining)
        take = waysFrom(i, remaining - coins[i]) if coins[i] <= remaining else 0
        return skip + take
    return waysFrom(0, amount)
```

- **Time**: `O(len(coins) × amount)` — each state solved once, O(1) work each.
- **Space**: `O(len(coins) × amount)` memo + up to `O(len(coins) + amount)` recursion depth.

If recursion depth is a worry for large `amount`, the bottom-up 1D DP (option B) gives the same time with `O(amount)` space and no stack — that's the only further optimization worth making here.

# Bottom-up 1D DP (option B)

Same problem, same `O(coins × amount)` time, but `O(amount)` space and no recursion stack.

## The mapping from A

Recursion A asked "for each coin, how many do I take." Bottom-up flips it: build a table `dp[x]` = number of combos summing to `x`, and **fold in one coin at a time**. The coin-on-the-outside loop is what enforces canonical ordering (= no permutations) — exactly the insight from step 4.

# 6. Outline

```python
def change(amount, coins):  # -> int
    """
    Reframe: process one denomination at a time; after fully folding coin c,
        dp[x] = combos for x using ONLY coins seen so far. Outer-coin loop
        is the canonical ordering that kills permutations.
    State: dp[x] = number of combinations summing to x. 1D because once a
        coin is folded in we never revisit it; we only need running counts.
    Invariant: after finishing coin c's pass, every dp[x] counts combos that
        use coins {first..c} in nondecreasing order.

    Core logic:
    - dp[0] = 1  (empty combination makes 0)
    - for each coin c:
        - for each amount x from c up to target:
            - any combo making (x - c) can be extended by one c to make x
            - dp[x] += dp[x - c]
    - answer = dp[amount]

    Edge cases:
    - amount == 0 -> dp[0] = 1 returned directly
    - coin larger than amount -> inner loop never runs, contributes nothing
    - impossible amount -> dp[amount] stays 0
    - inner loop MUST go low->high (ascending x) so a coin can be reused
      (unlimited supply); descending would cap each coin at one use
    """
```

# 7. Iterative implementation

**Skeleton** — table + the fold, stub the update:

```python
def change(amount, coins):
    dp = [0] * (amount + 1)
    dp[0] = 1                       # base: one way to make 0
    for c in coins:                 # fold one denomination at a time
        for x in range(...):        # which amounts this coin can affect
            dp[x] += ...            # combos extended by coin c
    return dp[amount]
```

**Iter 1** — fill the update. A combo for `x` using coin `c` = some combo for `x-c`, plus one `c`:

```python
def change(amount, coins):
    dp = [0] * (amount + 1)
    dp[0] = 1
    for c in coins:
        for x in range(c, amount + 1):   # start at c: below c, coin can't apply
            dp[x] += dp[x - c]           # extend every (x-c) combo with one c
    return dp[amount]
```

Core logic done. Walk the edges.

**Edge: ascending inner loop matters.** `range(c, amount+1)` already goes low→high. That ordering means when we compute `dp[x]`, `dp[x-c]` has *already* been updated with coin `c` this pass — so `c` can be used multiple times (unlimited supply). ✓ (Descending would mean each coin used at most once → that's the "coins-as-subset" variant, not this problem.)

**Edge: coin larger than amount** → `range(c, amount+1)` is empty, loop skips, no effect. ✓
**Edge: amount == 0** → `dp = [1]`, return `dp[0] = 1`. ✓
**Edge: impossible amount** → nothing ever writes `dp[amount]`, stays 0. ✓

# Trace on the by-hand example

`coins=[1,2,5]`, `amount=5`:

- start `dp = [1,0,0,0,0,0]`
- fold `1`: `dp = [1,1,1,1,1,1]`
- fold `2`: `dp = [1,1,2,2,3,3]`
- fold `5`: `dp = [1,1,2,2,3,4]`

→ `dp[5] = 4` ✓ (matches `5`, `2+2+1`, `2+1+1+1`, `1+1+1+1+1`)

# 8. Complexity

- **Time**: `O(len(coins) × amount)` — two nested loops, O(1) inner work.
- **Space**: `O(amount)` — single row, no recursion. This is the win over A.

No further optimization worth it; this is the tight canonical answer.