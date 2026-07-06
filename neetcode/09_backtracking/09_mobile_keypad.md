### question
You are given a string digits made up of digits from 2 through 9 inclusive.

Each digit (not including 1) is mapped to a set of characters as shown below:

A digit could represent any one of the characters it maps to.

Return all possible letter combinations that digits could represent. You may return the answer in any order.

We need return every string formed by choosing **one mapped letter per digit**, in the same digit order.

For example, with `digits = "23"`:

```text
2 -> a b c
3 -> d e f

choose one from 2, then one from 3:

ad
ae
af
bd
be
bf
cd
ce
cf
```

Output:

```python
["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
```

## Clarifying questions

In interview, I would confirm:

1. Can `digits` be empty?
   Usually yes. Return `[]`.

2. Are digits only from `2` to `9`?
   Problem says yes, so no need to handle `0` or `1`.

3. Can output be any order?
   Yes. We can return DFS order.

## Brainstorm solutions

### Solution 1: Backtracking DFS

Build combinations one character at a time.

For each digit:

```text
try every letter mapped to that digit
append it to current path
move to next digit
undo choice
```

This is the cleanest interview solution.

### Solution 2: Iterative expansion

Start with `[""]`.

For every digit, expand current combinations:

```text
[""] + "2" -> ["a", "b", "c"]
then "3" -> ["ad", "ae", "af", ...]
```

Also good, but backtracking is more common for combination-generation problems.

We choose **backtracking**, because it maps naturally to “make a choice, recurse, undo choice.”

---

## Implementation outline

```python
from typing import List

def letterCombinations(digits: str) -> List[str]:
    """
    Reframe: generate every path through digit-to-letter choices.

    State: current partial string and result list, chosen because we need
        to remember the prefix built so far and collect complete prefixes.

    Invariant: before exploring a digit, current path contains exactly one
        chosen letter for each earlier digit.

    lettersForDigit(digit) = all possible letters represented by this digit.

    Core logic:
    - if there are no digits, return no combinations
    - start with an empty path
    - explore the first digit
    - for every letter of the current digit:
        - choose that letter
        - explore the next digit
        - undo that letter
    - when path has one letter per digit, save the completed combination

    Edge cases:
    - empty input should return empty list
    - one digit returns each mapped letter as a one-letter string
    - digits with four letters, like seven and nine, should work naturally
    """
```

---

## Iteration 1: skeleton

```python
from typing import List

def letterCombinations(digits: str) -> List[str]:
    digit_to_letters = {
        "2": "abc",
        "3": "def",
        "4": "ghi",
        "5": "jkl",
        "6": "mno",
        "7": "pqrs",
        "8": "tuv",
        "9": "wxyz",
    }

    result = []
    path = []

    def backtrack(index: int) -> None:
        # TODO: if path is complete, save it
        # TODO: otherwise try each letter for current digit
        pass

    backtrack(0)
    return result
```

---

## Iteration 2: core happy path

Now fill the recursion.

```python
from typing import List

def letterCombinations(digits: str) -> List[str]:
    digit_to_letters = {
        "2": "abc",
        "3": "def",
        "4": "ghi",
        "5": "jkl",
        "6": "mno",
        "7": "pqrs",
        "8": "tuv",
        "9": "wxyz",
    }

    result = []
    path = []

    def backtrack(index: int) -> None:
        # Complete combination built
        if index == len(digits):
            result.append("".join(path))
            return

        current_digit = digits[index]
        letters = digit_to_letters[current_digit]

        for letter in letters:
            path.append(letter)        # choose
            backtrack(index + 1)       # explore
            path.pop()                 # undo

    backtrack(0)
    return result
```

Problem: for `digits = ""`, this returns `[""]`, but expected is usually `[]`.

So patch edge case.

---

## Final code

```python
from typing import List

def letterCombinations(digits: str) -> List[str]:
    """
    Reframe: generate every path through digit-to-letter choices.

    State: current partial string and result list, chosen because we need
        to remember the prefix built so far and collect complete prefixes.

    Invariant: before exploring a digit, current path contains exactly one
        chosen letter for each earlier digit.

    Core logic:
    - if there are no digits, return no combinations
    - start with an empty path
    - explore the first digit
    - for every letter of the current digit:
        - choose that letter
        - explore the next digit
        - undo that letter
    - when path has one letter per digit, save the completed combination

    Edge cases:
    - empty input should return empty list
    - one digit returns each mapped letter as a one-letter string
    - digits with four letters, like seven and nine, should work naturally
    """

    if not digits:
        return []

    digit_to_letters = {
        "2": "abc",
        "3": "def",
        "4": "ghi",
        "5": "jkl",
        "6": "mno",
        "7": "pqrs",
        "8": "tuv",
        "9": "wxyz",
    }

    result = []
    path = []

    def backtrack(index: int) -> None:
        if index == len(digits):
            result.append("".join(path))
            return

        current_digit = digits[index]

        for letter in digit_to_letters[current_digit]:
            path.append(letter)
            backtrack(index + 1)
            path.pop()

    backtrack(0)
    return result
```

## Edge case walkthrough

### Empty input

```python
digits = ""
```

Return:

```python
[]
```

Handled by:

```python
if not digits:
    return []
```

### One digit

```python
digits = "2"
```

Output:

```python
["a", "b", "c"]
```

DFS chooses each letter and immediately reaches base case.

### Four-letter digit

```python
digits = "7"
```

Output:

```python
["p", "q", "r", "s"]
```

Works because mapping stores `"pqrs"`.

## Complexity

Let `n = len(digits)`.

Each digit has at most `4` letters.

Maximum number of combinations:

```text
4^n
```

Each completed combination costs `O(n)` to join into a string.

Time:

```text
O(n * 4^n)
```

Space:

```text
O(n)
```

for recursion path, excluding output.

Including output storage:

```text
O(n * 4^n)
```
