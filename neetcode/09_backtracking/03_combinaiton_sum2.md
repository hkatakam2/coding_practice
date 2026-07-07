### question
You are given an array of integers candidates, which may contain duplicates, and a target integer target. Your task is to return a list of all unique combinations of candidates where the chosen numbers sum to target.

Each element from candidates may be chosen at most once within a combination. The solution set must not contain duplicate combinations.

You may return the combinations in any order and the order of the numbers in each combination can be in any order.

We need solve **Combination Sum II** style problem.

## 1. Restate

Given `candidates`, possibly with duplicate values, and `target`, return every **unique combination** whose sum is `target`.

Important differences from Combination Sum I:

1. Each array element can be used **at most once**.
2. `candidates` may contain duplicates.
3. Duplicate combinations must not appear in output.

Example:

```python
candidates = [10, 1, 2, 7, 6, 1, 5]
target = 8
```

Valid answer:

```python
[
    [1, 1, 6],
    [1, 2, 5],
    [1, 7],
    [2, 6]
]
```

---

## 2. Clarifying assumptions

I will assume the standard interview version:

```python
candidates contains positive integers
target is positive
```

That lets us sort and stop early when current number is already bigger than remaining target.

Input:

```python
List[int], int
```

Output:

```python
List[List[int]]
```

---

## 3. Walk example by hand

Input:

```python
candidates = [10, 1, 2, 7, 6, 1, 5]
target = 8
```

Sort first:

```python
[1, 1, 2, 5, 6, 7, 10]
```

Now build combinations:

Start with first `1`.

```python
path = [1], remaining = 7
```

Try next `1`.

```python
path = [1, 1], remaining = 6
```

Try `2`: remaining becomes `4`, no later value fits.

Try `5`: remaining becomes `1`, no later value fits.

Try `6`:

```python
path = [1, 1, 6], remaining = 0
```

Add it.

Backtrack.

From first `1`, try `2`.

```python
path = [1, 2], remaining = 5
```

Try `5`:

```python
path = [1, 2, 5], remaining = 0
```

Add it.

From first `1`, try `7`.

```python
path = [1, 7], remaining = 0
```

Add it.

Now back at top level.

There is another `1` at the same top level. Skip it, because starting with the second `1` would generate the same combinations as starting with the first `1`.

Then try `2`.

```python
path = [2], remaining = 6
```

Try `6`.

```python
path = [2, 6], remaining = 0
```

Add it.

Final:

```python
[[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
```

---

## 4. Brainstorm solutions

### Solution 1: Generate all subsets, then deduplicate

Generate every subset, check if sum equals target, put sorted tuple into a set.

Bad for interview:

```python
O(2^n * n)
```

Also awkward because duplicates require set cleanup.

### Solution 2: Backtracking with sorting and duplicate skipping

Sort the array.

At each recursive level, choose one candidate from the remaining suffix.

To avoid duplicate combinations:

```python
if i > start and candidates[i] == candidates[i - 1]:
    skip
```

Why this works:

At the same recursion depth, choosing the second duplicate as the “first choice” creates the same combination family as choosing the first duplicate.

This is the preferred solution.

---

## 5. Selected approach

Use sorted backtracking.

Core ideas:

1. Sort candidates.
2. Maintain current path.
3. Maintain remaining target.
4. At each level, iterate from `start` to end.
5. Skip duplicates at the same level.
6. Recurse with `i + 1`, because each element can be used once.
7. Stop early if candidate exceeds remaining target.

---

## 6. Plain-English implementation outline

```python
def combinationSum2(candidates, target):  # -> List[List[int]]
    """
    Reframe: sort first so duplicates become adjacent and can be skipped locally.

    State:
        - result: all valid combinations found so far
        - path: current combination being built
        - start: first index still allowed to choose
        - remaining: how much sum is still needed

    Invariant:
        path contains only candidates chosen from increasing indices,
        so no element is reused.

    isDuplicateChoice(i, start) =
        true when this candidate has same value as previous candidate
        and both are being considered at the same recursion level.

    Core logic:
    - sort candidates
    - start a depth-first search from the beginning
    - if remaining becomes zero, copy current path into result
    - otherwise, try each candidate from current allowed position onward
    - skip duplicate choices at same depth
    - stop trying larger numbers once candidate is bigger than remaining
    - choose candidate
    - recurse starting after chosen candidate
    - undo choice

    Edge cases:
    - no candidates
    - target cannot be formed
    - duplicate values in candidates
    - one candidate equals target
    - all candidates bigger than target
    - multiple copies needed, but each physical element can be used once
    """
```

---

## 7. Iterative implementation

### Iteration 1: Skeleton

```python
def combinationSum2(candidates, target):
    result = []
    path = []

    candidates.sort()

    def backtrack(start, remaining):
        pass

    backtrack(0, target)
    return result
```

We have the storage and sorted input. Now we need the base case.

---

### Iteration 2: Add successful base case

```python
def combinationSum2(candidates, target):
    result = []
    path = []

    candidates.sort()

    def backtrack(start, remaining):
        if remaining == 0:
            result.append(path.copy())
            return

    backtrack(0, target)
    return result
```

When `remaining == 0`, we found one valid combination.

Important: use `path.copy()`, not `path`, because `path` will keep changing during backtracking.

---

### Iteration 3: Add the choosing loop

```python
def combinationSum2(candidates, target):
    result = []
    path = []

    candidates.sort()

    def backtrack(start, remaining):
        if remaining == 0:
            result.append(path.copy())
            return

        for i in range(start, len(candidates)):
            value = candidates[i]

            path.append(value)
            backtrack(i + 1, remaining - value)
            path.pop()

    backtrack(0, target)
    return result
```

Key detail:

```python
backtrack(i + 1, remaining - value)
```

We use `i + 1` because each element can be used at most once.

If this were Combination Sum I, where values can be reused, we would recurse with `i`.

---

### Iteration 4: Add pruning

Because candidates are sorted and positive:

```python
if value > remaining:
    break
```

Full version:

```python
def combinationSum2(candidates, target):
    result = []
    path = []

    candidates.sort()

    def backtrack(start, remaining):
        if remaining == 0:
            result.append(path.copy())
            return

        for i in range(start, len(candidates)):
            value = candidates[i]

            if value > remaining:
                break

            path.append(value)
            backtrack(i + 1, remaining - value)
            path.pop()

    backtrack(0, target)
    return result
```

Now we avoid useless branches.

---

### Iteration 5: Add duplicate skipping

This is the most important part.

```python
if i > start and candidates[i] == candidates[i - 1]:
    continue
```

Meaning:

At the same recursion level, do not start a branch with the same value twice.

Final code:

```python
from typing import List

def combinationSum2(candidates: List[int], target: int) -> List[List[int]]:
    result = []
    path = []

    candidates.sort()

    def backtrack(start: int, remaining: int) -> None:
        if remaining == 0:
            result.append(path.copy())
            return

        for i in range(start, len(candidates)):
            value = candidates[i]

            # Skip duplicate choices at the same recursion depth.
            if i > start and candidates[i] == candidates[i - 1]:
                continue

            # Since sorted and positive, later values are also too large.
            if value > remaining:
                break

            path.append(value)
            backtrack(i + 1, remaining - value)
            path.pop()

    backtrack(0, target)
    return result
```

---

## 8. Why duplicate skipping works

Suppose sorted input is:

```python
[1, 1, 2, 5, 6, 7, 10]
```

At top level, we try the first `1`.

That branch can generate:

```python
[1, 1, 6]
[1, 2, 5]
[1, 7]
```

If we also try the second `1` at top level, it would generate duplicate versions of the same combinations.

So at the same depth:

```python
i > start and candidates[i] == candidates[i - 1]
```

means:

```python
"This value was already used as a starting choice at this level."
```

But we still allow `[1, 1, 6]`.

Why?

Because the second `1` is chosen in a deeper recursive call, not skipped at the same level.

For example:

```python
start = 0
choose candidates[0] = 1

then recursive call has start = 1

inside that call:
i = 1
i > start is false
so second 1 is allowed
```

That is the key distinction.

---

## 9. Edge cases

### Empty input

```python
candidates = []
target = 7
```

Output:

```python
[]
```

Loop never runs.

---

### No valid combination

```python
candidates = [2, 4, 6]
target = 5
```

Output:

```python
[]
```

No path reaches remaining `0`.

---

### All duplicates

```python
candidates = [1, 1, 1, 1]
target = 2
```

Output:

```python
[[1, 1]]
```

Not:

```python
[[1, 1], [1, 1], [1, 1], ...]
```

Duplicate skipping prevents repeated combinations.

---

### One value equals target

```python
candidates = [3, 5, 8]
target = 8
```

Output can include:

```python
[[8], [3, 5]]
```

---

### All values bigger than target

```python
candidates = [9, 10, 11]
target = 8
```

Output:

```python
[]
```

After sorting, first value is already too big, so we break immediately.

---

## 10. Complexity

Let `n = len(candidates)`.

Sorting:

```python
O(n log n)
```

Backtracking worst case:

```python
O(2^n)
```

Because each element has two broad possibilities: chosen or not chosen.

Copying valid combinations costs up to:

```python
O(n)
```

So worst-case time:

```python
O(2^n * n)
```

Space excluding output:

```python
O(n)
```

because recursion depth and `path` can grow up to `n`.

Space including output depends on how many valid combinations are returned.

Final answer:

```python
from typing import List

class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        result = []
        path = []

        candidates.sort()

        def backtrack(start: int, remaining: int) -> None:
            if remaining == 0:
                result.append(path.copy())
                return

            for i in range(start, len(candidates)):
                value = candidates[i]

                if i > start and candidates[i] == candidates[i - 1]:
                    continue

                if value > remaining:
                    break

                path.append(value)
                backtrack(i + 1, remaining - value)
                path.pop()

        backtrack(0, target)
        return result
```
