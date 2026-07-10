### question
Given an array nums of unique integers, return all possible subsets of nums.

The solution set must not contain duplicate subsets. You may return the solution in any order.

We need return **every subset** of a unique-integer array.

For example:

```python
nums = [1, 2, 3]
```

Possible subsets:

```python
[
  [],
  [1],
  [2],
  [3],
  [1, 2],
  [1, 3],
  [2, 3],
  [1, 2, 3]
]
```

Order does not matter.

---

## 1. Restate the problem

We are given an array `nums` where every integer is unique.

We need generate the **power set**: every possible subset of `nums`.

For each number, we have two choices:

1. do not include it
2. include it

So for `n` numbers, total subsets = `2^n`.

---

## 2. Clarifying questions

In interview, I would confirm:

1. Can `nums` be empty?

   * Usually yes. Then answer is `[[]]`.

2. Are values unique?

   * Yes, problem says unique integers.

3. Can output be in any order?

   * Yes.

4. Do we need avoid duplicate subsets?

   * Since nums are unique, normal backtracking naturally avoids duplicates.

---

## 3. Walk example by hand

Input:

```python
nums = [1, 2, 3]
```

At each number, choose include or skip.

Start:

```python
[]
```

After considering `1`:

```python
[]
[1]
```

After considering `2`:

```python
[]
[1]
[2]
[1, 2]
```

After considering `3`:

```python
[]
[1]
[2]
[1, 2]
[3]
[1, 3]
[2, 3]
[1, 2, 3]
```

Final answer has `8 = 2^3` subsets.

---

## 4. Brainstorm solutions

### Solution 1: Iterative expansion

Start with `[[]]`.

For every number, duplicate all existing subsets and add the number to the copies.

Example:

```python
res = [[]]

num = 1
res = [[], [1]]

num = 2
res = [[], [1], [2], [1, 2]]

num = 3
res = [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
```

Very simple and clean.

Time: `O(n * 2^n)`
Space: `O(n * 2^n)` for output.

---

### Solution 2: Backtracking

Build one subset path at a time.

At each index:

1. skip current number
2. include current number

This models the decision tree directly.

Time: `O(n * 2^n)`
Space: `O(n)` recursion stack, excluding output.

---

### Selected solution

Use **backtracking** because it explains the “include / exclude” decision clearly.

---

## 5. Implementation outline

```python
def subsets(nums):  # -> List[List[int]]
    """
    Reframe: every number creates a binary choice: include it or skip it.

    State: current subset path, chosen because we build one possible subset
        while walking through nums.

    Invariant: at index i, path contains decisions already made for nums before i.

    backtrack(index) = generate all subsets using nums from this index onward.

    Core logic:
    - start with empty path
    - at each number:
        - first explore the path where we skip this number
        - then explore the path where we include this number
    - when no numbers remain, save a copy of the current path

    Edge cases:
    - nums is empty: only subset is empty subset
    - nums has one element: answer is empty subset and singleton subset
    - negative numbers: no special handling
    - order of subsets does not matter
    """
```

---

## 6. Iterative implementation

### First skeleton

```python
from typing import List

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result = []
        path = []

        def backtrack(index):
            # TODO: if no numbers left, save current subset
            # TODO: skip current number
            # TODO: include current number
            pass

        backtrack(0)
        return result
```

---

### Fill base case

When `index == len(nums)`, we have made include/skip decisions for every number.

Important: append `path.copy()`, not `path`.

```python
from typing import List

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result = []
        path = []

        def backtrack(index):
            # changed: save a copy once all decisions are made
            if index == len(nums):
                result.append(path.copy())
                return

            # TODO: skip current number
            # TODO: include current number

        backtrack(0)
        return result
```

---

### Add skip branch

```python
from typing import List

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result = []
        path = []

        def backtrack(index):
            if index == len(nums):
                result.append(path.copy())
                return

            # changed: decision 1, skip nums[index]
            backtrack(index + 1)

            # TODO: include current number

        backtrack(0)
        return result
```

---

### Add include branch

When we include the current number:

1. add it to path
2. recurse
3. remove it before returning

That remove step is the backtracking cleanup.

```python
from typing import List

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result = []
        path = []

        def backtrack(index):
            if index == len(nums):
                result.append(path.copy())
                return

            # decision 1: skip nums[index]
            backtrack(index + 1)

            # changed: decision 2, include nums[index]
            path.append(nums[index])
            backtrack(index + 1)

            # changed: undo choice so sibling branches are clean
            path.pop()

        backtrack(0)
        return result
```

This is the complete core logic.

---

## 7. Edge cases

### Edge case 1: empty input

```python
nums = []
```

Call:

```python
backtrack(0)
```

Since `0 == len(nums)`, append copy of path:

```python
[[]]
```

Works.

---

### Edge case 2: one element

```python
nums = [5]
```

Branches:

```python
skip 5 -> []
include 5 -> [5]
```

Output:

```python
[[], [5]]
```

Works.

---

### Edge case 3: negative numbers

```python
nums = [-1, 2]
```

No arithmetic or sorting needed. We only include/skip values.

Works.

---

## 8. Final code

```python
from typing import List

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        """
        Reframe: every number creates a binary choice: include it or skip it.

        State: current subset path, chosen because we build one possible subset
            while walking through nums.

        Invariant: at index i, path contains decisions already made for nums before i.

        backtrack(index) = generate all subsets using nums from this index onward.

        Core logic:
        - start with empty path
        - at each number:
            - explore the path where we skip this number
            - explore the path where we include this number
        - when no numbers remain, save a copy of the current path

        Edge cases:
        - nums is empty: only subset is empty subset
        - nums has one element: answer is empty subset and singleton subset
        - negative numbers: no special handling
        - order of subsets does not matter
        """
        result = []
        path = []

        def backtrack(index: int) -> None:
            if index == len(nums):
                result.append(path.copy())
                return

            # Choice 1: skip nums[index]
            backtrack(index + 1)

            # Choice 2: include nums[index]
            path.append(nums[index])
            backtrack(index + 1)

            # Undo include choice
            path.pop()

        backtrack(0)
        return result
```

---

## Complexity

There are `2^n` subsets.

Each subset copy can cost up to `O(n)`.

Therefore:

```text
Time:  O(n * 2^n)
Space: O(n * 2^n)
```

The recursion stack alone is `O(n)`, but the returned output itself takes `O(n * 2^n)` space.
