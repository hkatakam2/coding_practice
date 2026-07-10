### question
Given a 2-D grid of characters board and a string word, return true if the word is present in the grid, otherwise return false.

For the word to be present it must be possible to form it with a path in the board with horizontally or vertically neighboring cells. The same cell may not be used more than once in a word.

## 1. Restate problem

We have a 2D character grid `board` and a string `word`.

Return `True` if we can trace the word in the grid by moving:

* up
* down
* left
* right

Rules:

* each next character must be horizontally/vertically adjacent
* same cell cannot be reused in the same word path
* path can start anywhere

This is the classic **DFS + backtracking** problem.

---

## 2. Clarifying questions

In interview I would ask:

1. Can `board` be empty?

   * I will handle empty board defensively.

2. Can `word` be empty?

   * Usually constraints say non-empty, but defensively: empty word is present, return `True`.

3. Are diagonal moves allowed?

   * No. Only horizontal/vertical.

4. Can we modify the board temporarily?

   * We could, but I’ll use a `visited` set first because clearer.

---

## 3. Example by hand

```python
board = [
    ["A","B","C","E"],
    ["S","F","C","S"],
    ["A","D","E","E"]
]

word = "ABCCED"
```

Start at `A`.

Path:

```text
A -> B -> C -> C -> E -> D
```

Coordinates:

```text
(0,0) A
(0,1) B
(0,2) C
(1,2) C
(2,2) E
(2,1) D
```

All are adjacent. No cell reused. Return `True`.

---

## 4. Brainstorm solutions

### Solution 1: Try every possible path

For every cell, try all possible paths of length `len(word)`.

This is basically DFS/backtracking.

Complexity:

```text
Time: O(rows * cols * 4^word_length)
Space: O(word_length)
```

Good enough for normal interview constraints.

---

### Solution 2: Trie?

Trie is useful if we search many words, like Word Search II.

Here we search only one word, so Trie is unnecessary.

---

### Selected solution

Use **DFS from every matching starting cell**.

At each DFS step:

* check current cell matches current word character
* mark cell as visited
* recursively try 4 neighbors for the next character
* unmark cell before returning

This is clean and easy to explain.

---

## 5. Implementation outline

```python
def exist(board, word):  # -> bool
    """
    Reframe: Search for one valid path spelling word.

    State: visited cells in current DFS path, chosen because
        we must prevent reusing the same board cell in one word path.

    Invariant: every cell in visited belongs to the current partial path,
        and that path spells the word prefix already matched.

    can_form_from(row, col, word_position) =
        whether word can be completed starting from this cell
        while matching the character at word_position.

    Core logic:
    - handle empty word
    - handle empty board
    - for every cell in board:
        - try to form the word starting there
        - if any start succeeds, return true
    - if no start succeeds, return false

    Helper logic:
    - if all characters are matched, return true
    - reject cell if outside board
    - reject cell if already used in this path
    - reject cell if character does not match current word character
    - mark current cell as used
    - try continuing into each neighboring cell
    - unmark current cell before returning
    - return whether any neighbor worked

    Edge cases:
    - empty word
    - empty board
    - word longer than number of cells
    - repeated letters requiring visited tracking
    - starting character appears many times
    - path almost works but would need to reuse a cell
    """
```

---

## 6. Iterative implementation

### Iteration 1: skeleton

```python
class Solution:
    def exist(self, board, word):
        def can_form_from(row, col, index):
            pass

        for row in range(len(board)):
            for col in range(len(board[0])):
                if can_form_from(row, col, 0):
                    return True

        return False
```

Problem: helper does nothing yet.

---

### Iteration 2: add base cases

```python
class Solution:
    def exist(self, board, word):
        rows = len(board)
        cols = len(board[0])

        def can_form_from(row, col, index):
            # matched the whole word
            if index == len(word):
                return True

            # outside board
            if row < 0 or row >= rows or col < 0 or col >= cols:
                return False

            # wrong character
            if board[row][col] != word[index]:
                return False

            # neighbor logic still missing
            return False

        for row in range(rows):
            for col in range(cols):
                if can_form_from(row, col, 0):
                    return True

        return False
```

Now we can reject bad cells, but cannot move yet.

---

### Iteration 3: add visited + backtracking

```python
class Solution:
    def exist(self, board, word):
        rows = len(board)
        cols = len(board[0])
        visited = set()

        def can_form_from(row, col, index):
            if index == len(word):
                return True

            if row < 0 or row >= rows or col < 0 or col >= cols:
                return False

            if (row, col) in visited:
                return False

            if board[row][col] != word[index]:
                return False

            visited.add((row, col))

            found = (
                can_form_from(row + 1, col, index + 1) or
                can_form_from(row - 1, col, index + 1) or
                can_form_from(row, col + 1, index + 1) or
                can_form_from(row, col - 1, index + 1)
            )

            visited.remove((row, col))

            return found

        for row in range(rows):
            for col in range(cols):
                if can_form_from(row, col, 0):
                    return True

        return False
```

Core logic complete.

---

## 7. Patch edge cases

### Edge case: empty word

```python
if word == "":
    return True
```

### Edge case: empty board

```python
if not board or not board[0]:
    return False
```

### Edge case: word longer than total cells

Impossible because same cell cannot be reused.

```python
if len(word) > rows * cols:
    return False
```

---

## Final code

```python
class Solution:
    def exist(self, board, word):
        if word == "":
            return True

        if not board or not board[0]:
            return False

        rows = len(board)
        cols = len(board[0])

        if len(word) > rows * cols:
            return False

        visited = set()

        def can_form_from(row, col, index):
            # We matched every character in word.
            if index == len(word):
                return True

            # Reject invalid board positions.
            if row < 0 or row >= rows or col < 0 or col >= cols:
                return False

            # Cannot reuse same cell in current path.
            if (row, col) in visited:
                return False

            # Current board cell must match current word character.
            if board[row][col] != word[index]:
                return False

            # Choose this cell.
            visited.add((row, col))

            # Explore four possible directions.
            found = (
                can_form_from(row + 1, col, index + 1) or
                can_form_from(row - 1, col, index + 1) or
                can_form_from(row, col + 1, index + 1) or
                can_form_from(row, col - 1, index + 1)
            )

            # Unchoose this cell so other paths can use it.
            visited.remove((row, col))

            return found

        for row in range(rows):
            for col in range(cols):
                if can_form_from(row, col, 0):
                    return True

        return False
```

---

## Complexity

Let:

```text
R = number of rows
C = number of columns
L = length of word
```

For each cell, DFS can branch up to 4 ways.

```text
Time: O(R * C * 4^L)
Space: O(L)
```

Space is `O(L)` because the recursion stack and `visited` set contain at most one cell per character in the word.

In practice, after the first move, we usually have at most 3 useful directions because we cannot go immediately back to the previous visited cell. So tighter intuition:

```text
O(R * C * 3^L)
```

But interview-safe answer:

```text
O(R * C * 4^L)
```
