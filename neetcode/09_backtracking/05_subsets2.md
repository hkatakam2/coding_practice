### question
You are given an array nums of integers, which may contain duplicates. Return all possible subsets.

The solution must not contain duplicate subsets. You may return the solution in any order.

## 1. Restate

We need return **all possible subsets** of `nums`.

`nums` may contain duplicates, but output must contain **no duplicate subsets**.

Example: choosing the first `2` or second `2` should not create duplicate `[2]`.

---

## 2. Clarifying / assumptions

I will assume:

* Empty subset `[]` is included.
* Each input element can be used at most once.
* Output order does not matter.
* Subset internal order does not matter, so sorting is allowed.

---

## 3. Example by hand

Input:

```python
nums = [1, 2, 2]
```

Sort first:

```python
[1, 2, 2]
```

Valid unique subsets:

```python
[
  [],
  [1],
  [1, 2],
  [1, 2, 2],
  [2],
  [2, 2]
]
```

Without duplicate handling, we might generate `[2]` twice:

* choose first `2`
* choose second `2`

So key rule:

> At the same recursion level, if we already tried value `2`, skip the next `2`.

---

## 4. Brainstorm solutions

### Solution 1: Generate everything, use set

Generate all subsets, convert each subset to tuple, store in set.

```python
set(tuple(subset))
```

Works, but not ideal because we create duplicates first, then remove them.

Complexity: still about `O(n * 2^n)`, but extra hashing and less clean.

---

### Solution 2: Sort + backtracking with duplicate skip

Sort `nums`.

While choosing the next element in a recursion level:

```python
if i > start and nums[i] == nums[i - 1]:
    continue
```

This says:

> If this duplicate value was already considered as the next choice at this same level, skip it.

This is the preferred interview solution.

---

## 5. Selected solution

Use backtracking.

At every node:

* add the current subset to result
* try adding each possible next number
* skip duplicate values at the same depth
* recurse
* undo the choice

---

## 6. Implementation outline

```python
from typing import List

def subsetsWithDup(nums: List[int]) -> List[List[int]]:
    """
    Reframe: sort first so duplicate values become adjacent, then skip repeated choices
    at the same recursion level.

    State:
    - result: all unique subsets collected so far
    - path: current subset being built
    - start: next index from where we are allowed to choose

    Invariant:
    - path is always built using increasing indexes
    - at each recursion level, the same value is chosen only once as the next element

    backtrack(start) = collect all unique subsets that extend current path
    using elements from start onward.

    Core logic:
    - sort nums
    - start with empty path
    - at every recursion call, save a copy of current path
    - try each possible next number from the remaining suffix
    - if this number is a duplicate of the previous number at the same level, skip it
    - otherwise choose it, recurse, then undo the choice

    Edge cases:
    - empty nums -> only empty subset
    - all duplicates -> should produce growing counts only, not repeated subsets
    - no duplicates -> behaves like normal subsets problem
    - negative numbers -> sorting still works
    """
```

---

## 7. Iterative implementation

### Iteration 1: skeleton

```python
from typing import List

def subsetsWithDup(nums: List[int]) -> List[List[int]]:
    nums.sort()

    result = []
    path = []

    def backtrack(start):
        # add current subset
        pass

        # try future choices
        pass

    backtrack(0)
    return result
```

---

### Iteration 2: core backtracking without duplicate skip

This generates subsets, but duplicate subsets may appear.

```python
from typing import List

def subsetsWithDup(nums: List[int]) -> List[List[int]]:
    nums.sort()

    result = []
    path = []

    def backtrack(start):
        # Every current path is a valid subset
        result.append(path.copy())

        # Try choosing every next possible number
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1)
            path.pop()

    backtrack(0)
    return result
```

For `[1, 2, 2]`, this can generate duplicate `[1, 2]` and duplicate `[2]`.

---

### Iteration 3: add duplicate skip

Final version:

```python
from typing import List

class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        nums.sort()

        result = []
        path = []

        def backtrack(start):
            # Current path itself is one valid subset
            result.append(path.copy())

            for i in range(start, len(nums)):
                # Skip duplicate choices at the same recursion level
                if i > start and nums[i] == nums[i - 1]:
                    continue

                path.append(nums[i])
                backtrack(i + 1)
                path.pop()

        backtrack(0)
        return result
```

---

## 8. Why duplicate skip works

Key line:

```python
if i > start and nums[i] == nums[i - 1]:
    continue
```

Meaning:

* `i > start` means we are not looking at the first option in this recursion level.
* `nums[i] == nums[i - 1]` means this value was already offered as a choice in this level.
* So choosing it again would create duplicate subset branches.

Example:

```python
nums = [1, 2, 2]
```

At root level:

```python
choose 1
choose 2
skip second 2
```

But inside the branch where we already chose first `2`, we are allowed to choose second `2` to form `[2, 2]`.

So this skip removes duplicate branches, not valid duplicate-value subsets.

---

## 9. Edge cases

### Empty input

```python
nums = []
```

Output:

```python
[[]]
```

Works because first `backtrack(0)` adds empty path.

---

### All duplicates

```python
nums = [2, 2, 2]
```

Output:

```python
[
  [],
  [2],
  [2, 2],
  [2, 2, 2]
]
```

The algorithm avoids repeated `[2]`, repeated `[2, 2]`, etc.

---

### No duplicates

```python
nums = [1, 2, 3]
```

Duplicate skip never triggers. Same as normal subsets.

---

### Negative numbers

```python
nums = [-1, -1, 2]
```

Sorting still groups duplicates:

```python
[-1, -1, 2]
```

Works normally.

---

## 10. Complexity

Sorting:

```python
O(n log n)
```

Number of possible unique subsets is at most:

```python
2^n
```

Copying each subset costs up to `O(n)`.

Total time:

```python
O(n * 2^n)
```

Space excluding output:

```python
O(n)
```

because recursion depth and `path` can grow to length `n`.

Space including output:

```python
O(n * 2^n)
```
