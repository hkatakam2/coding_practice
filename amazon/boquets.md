### question
Find the minimum day such that you can form at least m bouquets, each requiring k adjacent flowers that have bloomed (return -1 if impossible, e.g., when m*k > n).

## 1. Restate

We are given `bloomDay`, where `bloomDay[i]` is the day flower `i` blooms.

Need minimum day `d` such that we can make at least `m` bouquets.

Each bouquet needs exactly `k` **adjacent** bloomed flowers.

Return `-1` if impossible.

---

## 2. Clarifying assumptions

I would confirm:

* Can each flower be used in at most one bouquet?
  Yes.
* Does adjacency mean contiguous positions in the original array?
  Yes.
* Are bloom days positive integers?
  Usually yes.
* If `m * k > len(bloomDay)`, impossible?
  Yes, return `-1`.

---

## 3. Example by hand

```python
bloomDay = [1, 10, 3, 10, 2]
m = 2
k = 2
```

Need `2` bouquets, each needs `2` adjacent bloomed flowers.

Check day `3`:

```text
day 3 bloomed: [yes, no, yes, no, yes]
```

No two adjacent bloomed flowers.
Bouquets = `0`.

Check day `10`:

```text
day 10 bloomed: [yes, yes, yes, yes, yes]
```

We can take:

```text
[1, 10] as bouquet 1
[3, 10] as bouquet 2
```

Answer = `10`.

---

## 4. Brainstorm solutions

### Brute force

Try every possible day from `min(bloomDay)` to `max(bloomDay)`.
For each day, scan the array and count bouquets.

Complexity:

```text
O(n * maxDayRange)
```

Too slow if bloom days are large.

---

### Better solution: binary search on answer

Key observation:

If we can make `m` bouquets by day `d`, then we can also make them by any later day.

So feasibility is monotonic:

```text
day too small  -> cannot make bouquets
day large enough -> can make bouquets
```

That means binary search the minimum valid day.

Complexity:

```text
O(n log(maxBloomDay - minBloomDay))
```

This is the standard clean solution.

---

## 5. Selected implementation idea

We need helper:

```python
can_make(day)
```

It scans flowers left to right.

Maintain:

```text
adjacent_bloomed = number of consecutive flowers bloomed so far
bouquets = bouquets made so far
```

For each flower:

* If flower bloomed by `day`, increase `adjacent_bloomed`
* Else reset `adjacent_bloomed`
* When `adjacent_bloomed == k`, make one bouquet and reset `adjacent_bloomed`

Reset matters because flowers cannot be reused.

---

## 6. Plain-English outline

```python
def minDays(bloomDay, m, k):  # -> int
    """
    Reframe: binary search the earliest day where bouquet-making becomes possible.

    State:
    - bouquets: number of bouquets formed so far
    - consecutive: number of adjacent bloomed flowers in current run

    Invariant:
    - after scanning each flower, bouquets counts only non-overlapping bouquets
      formed from flowers bloomed by the chosen day.

    can_make(day) = returns whether at least m bouquets can be formed by this day.

    Core logic:
    - if total required flowers is more than available flowers, return -1
    - search between earliest bloom day and latest bloom day
    - for each middle day, ask whether we can make enough bouquets
    - if yes, try earlier days
    - if no, try later days
    - return earliest feasible day

    Edge cases:
    - m * k > number of flowers
    - k == 1, each bloomed flower can be one bouquet
    - all flowers bloom on same day
    - no valid adjacent groups until very late
    - already possible on minimum bloom day
    """
```

---

## 7. Iterative implementation

### Iteration 1: skeleton

```python
def minDays(bloomDay, m, k):
    if m * k > len(bloomDay):
        return -1

    def can_make(day):
        pass

    left = min(bloomDay)
    right = max(bloomDay)

    while left < right:
        mid = (left + right) // 2

        if can_make(mid):
            right = mid
        else:
            left = mid + 1

    return left
```

---

### Iteration 2: implement `can_make`

```python
def minDays(bloomDay, m, k):
    if m * k > len(bloomDay):
        return -1

    def can_make(day):
        bouquets = 0
        consecutive = 0

        for bloom in bloomDay:
            if bloom <= day:
                consecutive += 1

                if consecutive == k:
                    bouquets += 1
                    consecutive = 0

                    if bouquets == m:
                        return True
            else:
                consecutive = 0

        return False

    left = min(bloomDay)
    right = max(bloomDay)

    while left < right:
        mid = (left + right) // 2

        if can_make(mid):
            right = mid
        else:
            left = mid + 1

    return left
```

This is already complete.

---

## Final code

```python
def minDays(bloomDay, m, k):
    if m * k > len(bloomDay):
        return -1

    def can_make(day):
        bouquets = 0
        consecutive = 0

        for bloom in bloomDay:
            if bloom <= day:
                consecutive += 1

                if consecutive == k:
                    bouquets += 1
                    consecutive = 0  # use these k flowers, cannot reuse them

                    if bouquets >= m:
                        return True
            else:
                consecutive = 0

        return False

    left = min(bloomDay)
    right = max(bloomDay)

    while left < right:
        mid = (left + right) // 2

        if can_make(mid):
            right = mid
        else:
            left = mid + 1

    return left
```

---

## Complexity

Let:

```text
n = number of flowers
D = max(bloomDay) - min(bloomDay)
```

Each feasibility check scans all flowers:

```text
O(n)
```

Binary search over days:

```text
O(log D)
```

Total:

```text
Time: O(n log D)
Space: O(1)
```
