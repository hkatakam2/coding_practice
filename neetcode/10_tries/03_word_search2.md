### question

Given a 2-D grid of characters board and a list of strings words, return all words that are present in the grid.

For a word to be present it must be possible to form the word with a path in the board with horizontally or vertically neighboring cells. The same cell may not be used more than once in a word.

## 1. Restate the problem

We have:

```python
board: List[List[str]]
words: List[str]
```

Return all words from `words` that can be formed in the board.

A word is valid when:

* letters are connected horizontally or vertically
* one cell cannot be reused in the same word path
* return order can be any order

This is basically **Word Search I**, but for many words.

---

## 2. Clarifying assumptions

I’ll assume:

* `board` may be empty.
* `words` may be empty.
* Words should be returned once, even if they can be found multiple ways.
* Board contains normal characters, usually lowercase English letters.
* Output order does not matter.

---

## 3. Example by hand

```python
board = [
    ["o","a","a","n"],
    ["e","t","a","e"],
    ["i","h","k","r"],
    ["i","f","l","v"]
]

words = ["oath", "pea", "eat", "rain"]
```

Check `"oath"`:

```text
o -> a -> t -> h
(0,0) -> (0,1) -> (1,1) -> (2,1)
```

So `"oath"` exists.

Check `"eat"`:

```text
e -> a -> t
(1,3) -> (1,2) -> (1,1)
```

So `"eat"` exists.

`"pea"` and `"rain"` do not exist.

Output:

```python
["oath", "eat"]
```

---

## 4. Brainstorm solutions

### Solution A: Run DFS separately for every word

For each word, scan every board cell and try DFS.

Let:

```text
m = rows
n = cols
W = number of words
L = average word length
```

Complexity roughly:

```text
O(W * m * n * 4^L)
```

This is simple, but too repetitive. Many words share prefixes.

Example:

```python
["oath", "oak", "oar", "eat"]
```

Searching `"oa..."` repeatedly wastes work.

---

### Solution B: Trie + DFS from board

Put all words into a Trie.

Then start DFS from every board cell and walk the Trie at the same time.

The moment the board path does not match any Trie prefix, stop.

This is the standard clean solution.

Why Trie helps:

```text
words = ["oath", "oak", "oar"]

Trie shares prefix:
o -> a -> ...
```

So while exploring the board, we explore all matching words together.

Selected solution: **Trie + DFS/backtracking**

---

## 5. Implementation outline

```python
def findWords(board, words):  # -> List[str]
    """
    Reframe: Instead of searching each word separately, search all word prefixes at once.

    State:
    - Trie of all words, chosen because many words share prefixes.
    - result list for found words.
    - board cells temporarily marked visited during one DFS path.

    Invariant:
    - During DFS, the current board path matches the current Trie node prefix.
    - A board cell marked visited is already used in the current word path.

    buildTrie(words) = stores all words character by character.
    dfs(row, col, trieNode) = explores board paths that continue from trieNode.

    Core logic:
    - Build Trie from all words.
    - For each cell in the board:
        - Start DFS from that cell.
    - In DFS:
        - If current character is not a child in the Trie, stop.
        - Move into the child Trie node.
        - If this Trie node stores a completed word, add it to result.
        - Mark current board cell as visited.
        - Explore the four neighboring cells.
        - Restore current board cell.
        - Optionally prune empty Trie branches.

    Edge cases:
    - Empty board.
    - Empty words.
    - Word found multiple times.
    - Word is prefix of another word.
    - Single-cell board.
    - Word longer than total board cells.
    - Reusing same cell is not allowed.
    """
```

---

## 6. Iterative implementation

### Iteration 1: Skeleton

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None


class Solution:
    def findWords(self, board, words):
        root = TrieNode()

        # TODO: build Trie

        result = []

        # TODO: DFS from every cell

        return result
```

---

### Iteration 2: Build the Trie

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None


class Solution:
    def findWords(self, board, words):
        root = TrieNode()

        for word in words:
            node = root

            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()

                node = node.children[char]

            node.word = word

        result = []

        return result
```

At the end of a word, store the full word:

```python
node.word = word
```

That makes it easy to say: “we found a complete word.”

---

### Iteration 3: Add DFS happy path

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None


class Solution:
    def findWords(self, board, words):
        root = TrieNode()

        for word in words:
            node = root

            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()

                node = node.children[char]

            node.word = word

        result = []
        rows = len(board)
        cols = len(board[0])

        def dfs(row, col, node):
            char = board[row][col]

            if char not in node.children:
                return

            child = node.children[char]

            if child.word is not None:
                result.append(child.word)
                child.word = None

            board[row][col] = "#"

            directions = [
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1)
            ]

            for row_change, col_change in directions:
                next_row = row + row_change
                next_col = col + col_change

                if (
                    0 <= next_row < rows
                    and 0 <= next_col < cols
                    and board[next_row][next_col] != "#"
                ):
                    dfs(next_row, next_col, child)

            board[row][col] = char

        for row in range(rows):
            for col in range(cols):
                dfs(row, col, root)

        return result
```

This is already correct for normal cases.

Important line:

```python
child.word = None
```

This prevents duplicate output.

Example: if `"eat"` can be formed in two different ways, we only return it once.

---

### Iteration 4: Patch empty input edge cases

This line can crash if board is empty:

```python
cols = len(board[0])
```

So add:

```python
if not board or not board[0] or not words:
    return []
```

---

### Iteration 5: Optional Trie pruning optimization

After exploring a branch, if that Trie node has no children and no word, delete it from its parent.

This means once a word/prefix is fully exhausted, future DFS calls avoid it.

```python
if not child.children and child.word is None:
    del node.children[char]
```

---

## Final solution

```python
from typing import List


class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None


class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        """
        Reframe: Search all words together by searching valid Trie prefixes on the board.

        State:
        - Trie stores all target words.
        - DFS path uses temporary board marking to avoid reusing cells.
        - result stores found words.

        Invariant:
        - At each DFS call, the board path so far matches the Trie prefix represented
          by the current Trie node.

        Core logic:
        - Build Trie from words.
        - Start DFS from each board cell.
        - During DFS:
            - Stop if current character is not a valid next Trie character.
            - Move into the matching Trie child.
            - If that child completes a word, add it once.
            - Mark current board cell visited.
            - Explore neighbors.
            - Restore current board cell.
            - Prune dead Trie branches.

        Edge cases:
        - Empty board.
        - Empty words.
        - Same word found through multiple paths.
        - Word is prefix of another word.
        - Single-cell board.
        """

        if not board or not board[0] or not words:
            return []

        root = TrieNode()

        for word in words:
            node = root

            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()

                node = node.children[char]

            node.word = word

        result = []
        rows = len(board)
        cols = len(board[0])

        def dfs(row, col, node):
            char = board[row][col]

            if char not in node.children:
                return

            child = node.children[char]

            # Found a full word.
            if child.word is not None:
                result.append(child.word)

                # Prevent returning the same word multiple times.
                child.word = None

            # Mark current cell as used in this path.
            board[row][col] = "#"

            for row_change, col_change in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                next_row = row + row_change
                next_col = col + col_change

                if (
                    0 <= next_row < rows
                    and 0 <= next_col < cols
                    and board[next_row][next_col] != "#"
                ):
                    dfs(next_row, next_col, child)

            # Backtrack.
            board[row][col] = char

            # Optimization: remove exhausted Trie branch.
            if not child.children and child.word is None:
                del node.children[char]

        for row in range(rows):
            for col in range(cols):
                dfs(row, col, root)

        return result
```

---

## Complexity

Let:

```text
m = number of rows
n = number of columns
T = total number of characters across all words
L = maximum word length
```

Building the Trie:

```text
O(T)
```

DFS:

Worst case can still be large, but Trie pruning cuts many paths early.

Upper bound:

```text
O(m * n * 4^L)
```

More accurately, after the first move, each cell has at most 3 useful directions because we cannot immediately go back to the previous cell:

```text
O(m * n * 3^L)
```

Space:

```text
O(T)
```

for the Trie, plus recursion depth:

```text
O(L)
```

So total:

```text
O(T + L)
```

excluding the output list.
