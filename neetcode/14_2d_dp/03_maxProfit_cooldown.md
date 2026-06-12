## question
You are given an integer array `prices` where `prices[i]` is the price of NeetCoin on the `ith` day.
You may buy and sell one NeetCoin multiple times with the following restrictions:

* After you sell your NeetCoin, you cannot buy another one on the next day (i.e., there is a cooldown period of one day).
* You may only own at most one NeetCoin at a time.
You may complete as many transactions as you like.
Return the maximum profit you can achieve.

# 1. Restate

Array `prices`, `prices[i]` = price on day `i`. Buy/sell one coin many times. Constraints: hold ≤1 coin at a time; after selling, must skip the immediate next day before buying again (1-day cooldown). Max profit?

# 2. Clarifying questions

- `prices` empty or length 1 → profit 0?
- Prices non-negative ints? Can transaction be a no-op (do nothing)? → yes, baseline 0.
- Selling same day as buying allowed (0 profit)? → assume no, must be later day.
- Must end with no coin held (any profit comes from a sell)? → yes, unsold coin = no profit.

Assume: yes empty→0, no-op allowed, sell strictly after buy.

# 3. Example by hand

`prices = [1, 2, 3, 0, 2]`

- Buy day0 (1), sell day1 (2) → +1. Cooldown day2. Buy day3 (0), sell day4 (2) → +2. Total **3**.
- Alt: buy0(1) sell2(3)=+2, cooldown3, can't buy4 til... buy nothing → 2. Worse.

Answer = **3**.

# 4. Brainstorm + complexity

Decision each day depends on a *state*: do I currently hold a coin, am I free to buy, or am I in cooldown? Classic state machine.

Three states per day:
- **hold**: own a coin
- **sold**: just sold today (→ cooldown tomorrow)
- **rest**: own nothing, free to buy (not in cooldown)

Options:
- (A) **Brute force recursion** over buy/sell/skip decisions → exponential `O(2^n)`. Matches step-3 by-hand "try every path."
- (B) **DP / state machine**, track best profit in each state per day → `O(n)` time, `O(1)` space.

# 5. Solutions

- **Solution A (brute force, mirrors by-hand):** recurse day-by-day choosing actions, track holding + cooldown. Clear but exponential.
- **Solution B (state machine DP):** maintain three running values `hold/sold/rest`, transition each day. Simple, linear, easy to explain.

I'd recommend **B**. Which do you want to implement?

# 6. Outline

```python
def maxProfit(prices):  # -> int
    """
    Reframe: each day you're in one of 3 states; track best profit reachable in each, sweep forward.
    State: three running profits —
        hold = best profit while currently owning a coin,
        sold = best profit on a day you just sold (next day forced cooldown),
        rest = best profit owning nothing & free to act.
      chosen because the cooldown rule only looks back one day, so a fixed
      set of states + last-day values fully captures the future decision.
    Invariant: after processing day i, each of hold/sold/rest = best profit
      ending day i in that state.

    transition(price) = update the three states from yesterday's values.

    Core logic:
    - start: not holding, no profit; holding costs us a buy
    - each day, recompute each state from yesterday's states:
        to hold today: stay holding, OR buy today (only from rest, never from sold→cooldown)
        to be sold today: must sell a coin held yesterday
        to rest today: stay resting, OR yesterday was a sold day (cooldown ends)
    - answer: best of "ended not holding" = max(sold, rest)

    Edge cases:
    - empty prices -> 0
    - single day -> can't sell -> 0
    """
```

# 7. Iterative implementation

**Iter 1 — skeleton from plain English**

```python
def maxProfit(prices):
    # three states, seeded for "before day 0"
    hold = ...   # owning a coin
    sold = ...   # just sold today
    rest = ...   # free, owning nothing

    for price in prices:
        # recompute each from yesterday's values
        hold = best(stay holding, buy today from rest)
        sold = best(sell coin held yesterday)
        rest = best(stay resting, cooldown ended from sold)
    return max(sold, rest)
```

**Iter 2 — seed values + fill transitions**

Holding before any day is impossible → seed `hold = -inf`. `sold`/`rest` = 0.

```python
def maxProfit(prices):
    hold = float('-inf')   # can't hold before buying
    sold = 0
    rest = 0

    for price in prices:
        prev_hold, prev_sold, prev_rest = hold, sold, rest   # snapshot yesterday
        hold = max(prev_hold, prev_rest - price)   # keep holding, or buy from rest
        sold = prev_hold + price                   # sell what we held
        rest = max(prev_rest, prev_sold)           # stay free, or cooldown lifts
    return max(sold, rest)
```

Snapshot needed so updates use *yesterday's* values, not this-iteration's.

Core logic done. Now edge cases.

**Iter 3 — walk edges**

- *empty prices*: loop never runs → returns `max(0,0)=0`. ✓ already handled.
- *single day*: loop runs once, `sold = -inf + price = -inf`, `rest = 0` → `max(-inf, 0) = 0`. ✓ already handled.

No patches needed.

```python
def maxProfit(prices):  # -> int
    hold = float('-inf')
    sold = 0
    rest = 0
    for price in prices:
        prev_hold, prev_sold, prev_rest = hold, sold, rest
        hold = max(prev_hold, prev_rest - price)
        sold = prev_hold + price
        rest = max(prev_rest, prev_sold)
    return max(sold, rest)
```

# 8. Complexity

- **Time** `O(n)` — single sweep, constant work per day.
- **Space** `O(1)` — three scalars, no array.

Already optimal. The state-machine collapse (vs an `O(n)` array of states) is the only "optimization," and it falls out naturally from noticing each day depends only on yesterday.