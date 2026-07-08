### question
You are given an array of distinct integers nums and a target integer target. Your task is to return a list of all unique combinations of nums where the chosen numbers sum to target.

The same number may be chosen from nums an unlimited number of times. Two combinations are the same if the frequency of each of the chosen numbers is the same, otherwise they are different.

You may return the combinations in any order and the order of the numbers in each combination can be in any order.

We need solve **Combination Sum**.

Given distinct integers `nums` and `target`, return all unique combinations where numbers sum to `target`.

Important assumption: `nums` contains **positive integers**. With `0` or negative numbers and unlimited reuse, the number of combinations can become infinite.

---

## 1. Restate

We can pick each number **unlimited times**.
Need all combinations whose sum equals `target`.
Combination uniqueness is based on frequency, so:

```python
[2, 2, 3]
```

is same as:

```python
[3, 2, 2]
```

So we must avoid permutation duplicates.

---

## 2. Clarifying questions

In interview I would confirm:

1. Are all numbers positive?
   I assume yes.

2. Can we return combinations in any order?
   Yes.

3. Can each individual combination be in any order?
   Yes, but we will generate them in sorted / nondecreasing order to avoid duplicates.

---

## 3. Example by hand

Input:

```python
nums = [2, 3, 6, 7]
target = 7
```

Possible:

```python
2 + 2 + 3 = 7
7 = 7
```

Invalid:

```python
2 + 3 + 2
```

Same frequency as `[2, 2, 3]`, so duplicate.

Output:

```python
[[2, 2, 3], [7]]
```

---

## 4. Brainstorm solutions

### Solution 1: brute force all sequences

Try every possible sequence until sum exceeds target.

Problem: creates duplicates:

```python
[2, 2, 3]
[2, 3, 2]
[3, 2, 2]
```

Harder to deduplicate cleanly.

Time: bad, lots of duplicate work.

---

### Solution 2: backtracking with index

At each recursive step, only choose from current index onward.

This means once we choose `3`, we never go back and choose `2`.

So paths are naturally nondecreasing:

```python
[2, 2, 3]
```

but never:

```python
[2, 3, 2]
```

This removes duplicate permutations.

This is the clean interview solution.

---

## 5. Selected solution

Use DFS / backtracking.

At each helper call:

```python
dfs(start_index, remaining_sum, current_combination)
```

Meaning:

* `start_index`: first number we are allowed to choose
* `remaining_sum`: how much more we need to reach target
* `current_combination`: numbers chosen so far

For every number from `start_index` onward:

* choose it
* recurse with same index, because reuse is allowed
* undo choice

If `remaining_sum == 0`, save current combination.

If candidate is greater than remaining sum, stop because array is sorted.

---

## 6. Implementation outline

```python
def combinationSum(nums, target):  # -> List[List[int]]
    """
    Reframe: build combinations in nondecreasing candidate order, so permutations never appear.

    State: current path and remaining target.
        path holds current combination.
        remaining tells how far we are from target.
        start index prevents going backward to smaller candidates.

    Invariant: path is always built using candidates from left to right.
        Therefore same frequency-combination is generated once.

    dfs(start, remaining) = find all ways to finish current path using nums[start:].

    Core logic:
    - sort nums so we can prune when candidate is too large
    - start with empty path and full target
    - recursively try each allowed candidate
    - reuse candidate by passing same index again
    - avoid permutation duplicates by never using candidates before start
    - when remaining becomes zero, copy path into answer

    Edge cases:
    - target is zero: return one empty combination or [] depending platform; usually [[]]
    - nums is empty: no combinations unless target is zero
    - candidate larger than remaining: stop loop
    - no possible combination: return []
    - repeated nums not expected, but sorting still works; if duplicates existed we'd need skip duplicates
    """
```

---

## 7. Iterative implementation

### Step 1: skeleton

```python
def combinationSum(nums, target):
    nums.sort()
    result = []
    path = []

    def dfs(start, remaining):
        pass

    dfs(0, target)
    return result
```

---

### Step 2: add base case

```python
def combinationSum(nums, target):
    nums.sort()
    result = []
    path = []

    def dfs(start, remaining):
        # If current path sums exactly to target
        if remaining == 0:
            result.append(path.copy())
            return

    dfs(0, target)
    return result
```

---

### Step 3: try each candidate

```python
def combinationSum(nums, target):
    nums.sort()
    result = []
    path = []

    def dfs(start, remaining):
        if remaining == 0:
            result.append(path.copy())
            return

        for i in range(start, len(nums)):
            candidate = nums[i]

            # TODO: choose candidate
            # TODO: recurse
            # TODO: undo choice

    dfs(0, target)
    return result
```

---

### Step 4: fill choose / recurse / undo

Key point:

```python
dfs(i, remaining - candidate)
```

Pass `i`, not `i + 1`, because same number can be reused.

```python
def combinationSum(nums, target):
    nums.sort()
    result = []
    path = []

    def dfs(start, remaining):
        if remaining == 0:
            result.append(path.copy())
            return

        for i in range(start, len(nums)):
            candidate = nums[i]

            path.append(candidate)
            dfs(i, remaining - candidate)
            path.pop()

    dfs(0, target)
    return result
```

This works logically, but still explores negative remaining values.

---

### Step 5: patch pruning edge case

Since `nums` sorted, once candidate is too big, all later candidates are also too big.

```python
def combinationSum(nums, target):
    nums.sort()
    result = []
    path = []

    def dfs(start, remaining):
        if remaining == 0:
            result.append(path.copy())
            return

        for i in range(start, len(nums)):
            candidate = nums[i]

            if candidate > remaining:
                break

            path.append(candidate)
            dfs(i, remaining - candidate)
            path.pop()

    dfs(0, target)
    return result
```

This is the final clean version.

---

## Final Python solution

```python
from typing import List

class Solution:
    def combinationSum(self, nums: List[int], target: int) -> List[List[int]]:
        nums.sort()
        result = []
        path = []

        def dfs(start: int, remaining: int) -> None:
            if remaining == 0:
                result.append(path.copy())
                return

            for i in range(start, len(nums)):
                candidate = nums[i]

                if candidate > remaining:
                    break

                path.append(candidate)

                # Use i again because candidate can be reused unlimited times.
                dfs(i, remaining - candidate)

                path.pop()

        dfs(0, target)
        return result
```

---

## Walk through code on example

```python
nums = [2, 3, 6, 7]
target = 7
```

Sorted:

```python
[2, 3, 6, 7]
```

DFS explores:

```python
choose 2 -> remaining 5
    choose 2 -> remaining 3
        choose 2 -> remaining 1
            stop, all candidates too large
        choose 3 -> remaining 0
            save [2, 2, 3]

choose 3 -> remaining 4
    choose 3 -> remaining 1
        stop

choose 6 -> remaining 1
    stop

choose 7 -> remaining 0
    save [7]
```

Result:

```python
[[2, 2, 3], [7]]
```

---

## Complexity

Let:

```python
n = len(nums)
T = target
m = minimum number in nums
```

Maximum depth is about:

```python
T / m
```

because we keep subtracting at least `m`.

Time complexity is output-sensitive/exponential:

```python
O(number_of_valid_and_partial_combinations * average_combination_length)
```

A common loose bound:

```python
O(n^(T / m))
```

Space complexity:

```python
O(T / m)
```

for recursion/path, excluding output.

Including output:

```python
O(total size of all returned combinations)
```
