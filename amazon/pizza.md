### question
Given base pizza prices and topping prices, determine which total price closest to a target budget can be achieved by choosing one base and any combination of toppings (with limited repeats per topping)

## 1. Restate

We are given:

```python
baseCosts: list[int]
toppingCosts: list[int]
target: int
```

We must choose:

```text
exactly one base
plus each topping 0, 1, or 2 times
```

Return the total cost closest to `target`.

Tie rule:

```text
if two totals are equally close, return the smaller total
```

---

## 2. Example by hand

```python
baseCosts = [10]
toppingCosts = [1, 3]
target = 13
```

Start with base `10`.

For topping `1`, choose:

```text
0 times -> 10
1 time  -> 11
2 times -> 12
```

Then topping `3`:

```text
10 + 0 = 10
10 + 3 = 13
10 + 6 = 16

11 + 0 = 11
11 + 3 = 14
11 + 6 = 17

12 + 0 = 12
12 + 3 = 15
12 + 6 = 18
```

Closest to `13` is:

```text
13
```

Return:

```python
13
```

---

## 3. Brainstorm solutions

### Brute force

Try every base and every topping combination.

Each topping has 3 choices:

```text
0 copies, 1 copy, 2 copies
```

So total combinations:

```text
baseCount * 3^toppingCount
```

This is simple and usually acceptable because topping count is small in this problem.

### DP / set of possible sums

Build all possible topping sums using a set, then combine with every base.

Also fine, but backtracking is more natural in interviews.

I’d choose **DFS/backtracking** because it is simple, readable, and easy to explain.

---

## 4. Selected approach

For each base:

```text
start total = base
recursively decide how many times to use each topping
after each total, update best answer
```

Because all costs are positive:

```text
if current total is already >= target,
adding more toppings only increases the total,
so we can stop exploring that branch
```

But before stopping, we still update the best answer.

---

## 5. Implementation outline

```python
def closest_cost(baseCosts, toppingCosts, target):  # -> int
    """
    Reframe: Try all topping-choice paths for every base and keep closest total.

    State:
    - best total seen so far
    - current topping index
    - current accumulated price

    Invariant:
    - best is always the closest total among all combinations explored so far.

    is_better(candidate, best) =
        candidate is closer to target than best,
        or equally close but smaller.

    explore(topping, current_total) =
        try choosing this topping 0, 1, or 2 times,
        then move to next topping.

    Core logic:
    - initialize best using one base
    - for each base:
        - start recursive exploration from that base price
    - at every recursive state:
        - update best using current total
        - if all toppings are considered, stop
        - if current total already reaches or passes target, stop
        - otherwise try taking current topping 0, 1, or 2 times

    Edge cases:
    - no toppings
    - base alone is closest
    - exact target found
    - tie between lower and higher cost
    - all totals are above target
    - all totals are below target
    """
```

---

## 6. Iteration 1: skeleton

```python
def closest_cost(baseCosts, toppingCosts, target):
    best = baseCosts[0]

    def is_better(candidate, current_best):
        pass

    def explore(topping_index, current_total):
        pass

    for base in baseCosts:
        explore(0, base)

    return best
```

---

## 7. Iteration 2: implement comparison helper

```python
def closest_cost(baseCosts, toppingCosts, target):
    best = baseCosts[0]

    def is_better(candidate, current_best):
        candidate_diff = abs(candidate - target)
        best_diff = abs(current_best - target)

        if candidate_diff < best_diff:
            return True

        if candidate_diff == best_diff and candidate < current_best:
            return True

        return False

    def explore(topping_index, current_total):
        pass

    for base in baseCosts:
        explore(0, base)

    return best
```

---

## 8. Iteration 3: implement DFS core logic

```python
def closest_cost(baseCosts, toppingCosts, target):
    best = baseCosts[0]

    def is_better(candidate, current_best):
        candidate_diff = abs(candidate - target)
        best_diff = abs(current_best - target)

        if candidate_diff < best_diff:
            return True

        if candidate_diff == best_diff and candidate < current_best:
            return True

        return False

    def explore(topping_index, current_total):
        nonlocal best

        # Every current total is a valid combination,
        # because choosing no more toppings is allowed.
        if is_better(current_total, best):
            best = current_total

        # Exact target is the best possible.
        if best == target:
            return

        # No more toppings to choose.
        if topping_index == len(toppingCosts):
            return

        # Since toppings are positive, going higher only moves farther
        # once we are already at or above target.
        if current_total >= target:
            return

        topping_price = toppingCosts[topping_index]

        # choose this topping 0, 1, or 2 times
        explore(topping_index + 1, current_total)
        explore(topping_index + 1, current_total + topping_price)
        explore(topping_index + 1, current_total + 2 * topping_price)

    for base in baseCosts:
        explore(0, base)

    return best
```

---

## 9. Final code

```python
def closest_cost(baseCosts, toppingCosts, target):
    best = baseCosts[0]

    def is_better(candidate, current_best):
        candidate_diff = abs(candidate - target)
        best_diff = abs(current_best - target)

        if candidate_diff < best_diff:
            return True

        if candidate_diff == best_diff and candidate < current_best:
            return True

        return False

    def explore(topping_index, current_total):
        nonlocal best

        if is_better(current_total, best):
            best = current_total

        if best == target:
            return

        if topping_index == len(toppingCosts):
            return

        if current_total >= target:
            return

        topping_price = toppingCosts[topping_index]

        for count in range(3):
            next_total = current_total + count * topping_price
            explore(topping_index + 1, next_total)

    for base in baseCosts:
        explore(0, base)

    return best
```

---

## 10. Edge cases checked

### No toppings

```python
baseCosts = [3, 10]
toppingCosts = []
target = 8
```

Only possible totals:

```text
3, 10
```

Both distance:

```text
abs(3 - 8) = 5
abs(10 - 8) = 2
```

Return:

```python
10
```

Code handles it because DFS immediately stops when `topping_index == len(toppingCosts)`.

---

### Tie, choose smaller

```python
baseCosts = [4]
toppingCosts = [2]
target = 7
```

Possible totals:

```text
4, 6, 8
```

`6` and `8` are both distance `1`.

Return:

```python
6
```

The helper handles this:

```python
candidate_diff == best_diff and candidate < current_best
```

---

### Exact target

```python
baseCosts = [5]
toppingCosts = [2, 3]
target = 10
```

Possible:

```text
5 + 2 + 3 = 10
```

Return immediately once best is target.

---

### Base alone is closest

```python
baseCosts = [9]
toppingCosts = [5, 6]
target = 10
```

Base alone is `9`.

Adding toppings gives `14`, `15`, etc.

Return:

```python
9
```

Code handles it because every recursive state updates `best`, including the base-only state.

---

## 11. Complexity

Let:

```text
n = number of bases
m = number of toppings
```

Each topping has 3 choices:

```text
0, 1, 2
```

So time complexity:

```text
O(n * 3^m)
```

Recursive call stack depth:

```text
O(m)
```

Space complexity:

```text
O(m)
```

The pruning:

```python
if current_total >= target:
    return
```

can reduce runtime in practice, but worst case remains:

```text
O(n * 3^m)
```
