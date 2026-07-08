### question
Given an array nums of unique integers, return all the possible permutations. You may return the answer in any order.


We need return **all orderings** of `nums`.

Example:
`nums = [1, 2, 3]`

Output can be:

```python
[
  [1, 2, 3],
  [1, 3, 2],
  [2, 1, 3],
  [2, 3, 1],
  [3, 1, 2],
  [3, 2, 1],
]
```

Because `nums` has unique integers, no duplicate-handling needed.

---

## 1. Clarify

Inputs:

```python
nums: List[int]
```

Output:

```python
List[List[int]]
```

Assumptions:

* `nums` contains unique integers.
* Each permutation uses every number exactly once.
* Any output order is okay.

---

## 2. Hand example

For:

```python
nums = [1, 2, 3]
```

Start with empty path:

```python
[]
```

Choose `1`:

```python
[1]
```

Remaining choices: `2`, `3`.

Choose `2`:

```python
[1, 2]
```

Remaining choice: `3`.

Choose `3`:

```python
[1, 2, 3]
```

Length is now same as `nums`, so save it.

Then undo last choice and try another choice.

This is classic **backtracking**.

---

## 3. Brainstorm solutions

### Solution 1: Backtracking with `used` set/list

Maintain:

* current permutation path
* which numbers are already used

At each step:

* try every unused number
* add it to path
* recurse
* remove it from path

This is simple and interview-friendly.

Time:

```python
O(n * n!)
```

Because there are `n!` permutations, and copying each one costs `O(n)`.

Space excluding output:

```python
O(n)
```

For recursion stack, path, and used array.

---

### Solution 2: In-place swapping

Swap each number into the current position.

This avoids a separate `used` array, but mutation logic is slightly trickier.

Also:

```python
O(n * n!)
```

Good, but less beginner-readable.

---

### Selected solution

Use **backtracking with used array** because it is clearest.

---

## 4. Plain English outline

```python
def permute(nums):  # -> List[List[int]]
    """
    Reframe: build one permutation position by position.

    State:
    - path: current partial permutation
    - used: whether each number is already inside path
    - result: completed permutations

    chosenAlready(index) = whether nums[index] is already in path.

    Core logic:
    - start with empty path
    - if path already contains all numbers:
        - copy path into result
        - stop this branch
    - otherwise:
        - try every number
        - skip number if already used
        - choose number
        - recurse to fill next position
        - undo choice

    Edge cases:
    - empty nums => one permutation: [[]]
    - one number => [[that number]]
    - nums has negative numbers => no issue
    - nums has zero => no issue
    """
```

---

## 5. Iteration 1: skeleton

```python
from typing import List

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result = []
        path = []
        used = [False] * len(nums)

        def backtrack():
            pass

        backtrack()
        return result
```

---

## 6. Iteration 2: base case

When `path` has all numbers, save a copy.

```python
from typing import List

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result = []
        path = []
        used = [False] * len(nums)

        def backtrack():
            # changed: added completed permutation condition
            if len(path) == len(nums):
                result.append(path.copy())
                return

        backtrack()
        return result
```

Important: use `path.copy()`, not `path`, because `path` keeps changing during backtracking.

---

## 7. Iteration 3: try every unused number

```python
from typing import List

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result = []
        path = []
        used = [False] * len(nums)

        def backtrack():
            if len(path) == len(nums):
                result.append(path.copy())
                return

            # changed: try every candidate number
            for i in range(len(nums)):
                if used[i]:
                    continue

                path.append(nums[i])
                used[i] = True

                backtrack()

                path.pop()
                used[i] = False

        backtrack()
        return result
```

This is already complete.

---

## Final code

```python
from typing import List

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result = []
        path = []
        used = [False] * len(nums)

        def backtrack():
            if len(path) == len(nums):
                result.append(path.copy())
                return

            for i in range(len(nums)):
                if used[i]:
                    continue

                # choose
                path.append(nums[i])
                used[i] = True

                # explore
                backtrack()

                # undo
                path.pop()
                used[i] = False

        backtrack()
        return result
```

---

## Edge case walk

### Case 1: empty input

```python
nums = []
```

Initially:

```python
path = []
```

Since `len(path) == len(nums)`, we append:

```python
[]
```

Output:

```python
[[]]
```

This is correct mathematically: there is one permutation of an empty list.

---

### Case 2: one element

```python
nums = [5]
```

Output:

```python
[[5]]
```

No patch needed.

---

### Case 3: negative numbers

```python
nums = [-1, 2]
```

Output:

```python
[[-1, 2], [2, -1]]
```

No patch needed because values do not matter.

---

## Complexity

Let `n = len(nums)`.

There are:

```python
n!
```

permutations.

Each completed permutation is copied in `O(n)` time.

So total time:

```python
O(n * n!)
```

Extra space excluding output:

```python
O(n)
```

Output space:

```python
O(n * n!)
```
