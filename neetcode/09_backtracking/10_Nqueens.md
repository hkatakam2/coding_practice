### question
The n-queens puzzle is the problem of placing n queens on an n x n chessboard so that no two queens can attack each other.

A queen in a chessboard can attack horizontally, vertically, and diagonally.

Given an integer n, return all distinct solutions to the n-queens puzzle.

Each solution contains a unique board layout where the queen pieces are placed. 'Q' indicates a queen and '.' indicates an empty space.

You may return the answer in any order.

**1. Restating the question**
Place `n` queens on an `n x n` board. No two queens attack each other. Attack means same row, column, or diagonal. Return all valid board layouts as lists of strings (`Q` for queen, `.` for empty). Order doesn't matter.

**2. Clarifying questions & I/O**

* Input: `n` (integer).
* Output: List of list of strings.
* Constraints? `1 <= n <= 9` typical.
* Valid to return empty list? Yes, if no solution exists (e.g., `n = 2`).
* Rotations/reflections distinct? Yes, treat as distinct arrays.

**3. By-hand example**
`n = 4`.
Row 0: Place queen at (0, 0).
Row 1: (1, 0) attacked. (1, 1) attacked. Place at (1, 2).
Row 2: (2, 0) attacked. (2, 1) attacked. (2, 2) attacked. (2, 3) attacked. Dead end.
Backtrack!
Row 1: Move queen to (1, 3).
Row 2: Place at (2, 0).
Row 3: Place at (3, 2).
Valid board 1 found: `[".Q..", "...Q", "Q...", "..Q."]`

**4. Brainstorming & Complexity**

* *Brute Force*: Generate all combinations of placing `n` queens in `n*n` spots. Filter valid ones. Time: $O((N^2 \text{ choose } N))$. Horrible.
* *Backtracking (Row-by-Row)*: Place 1 queen per row. Try every column. Check validity against previous rows. Time: $O(N!)$ worst case. Space: $O(N)$ for recursion stack.
* *Backtracking with Sets*: Same as above, but use Hash Sets to track attacked columns and diagonals. Diagonals have a neat math property:
* Positive diagonal (bottom-left to top-right): `row + col` is constant.
* Negative diagonal (top-left to bottom-right): `row - col` is constant.
Time: $O(N!)$, Space: $O(N)$.



**5. Suggest Solutions**
Prefer Backtracking with Sets. Simple, mathematical, easy to explain. Tracks state cleanly without complex grid traversals. Mimics hand-solving perfectly.

**6. Outline**

```python
def solveNQueens(n: int): # -> List[List[str]]
    """
    Reframe: Place one queen per row; track attacked columns and diagonals mathematically.
    State: sets for `cols`, `pos_diags` (r+c), `neg_diags` (r-c), chosen because diagonals share constant sum/difference properties.
    Invariant: Above current row, all placed queens are mutually safe.

    is_safe(row, col) = checks if col or diags exist in attacked sets.
    place_queen(row, col) = adds queen to board and updates attacked sets.
    remove_queen(row, col) = removes queen from board and attacked sets.
    format_board() = converts internal state to required string format.

    Core logic:
    - If current row equals n, format board and append to results.
    - For each column in current row:
        - If is_safe(current row, current col):
            - place_queen(current row, current col)
            - recurse to next row
            - remove_queen(current row, current col)
            
    Edge cases:
    - n = 2 or n = 3 (impossible to solve, should return empty).
    - n = 1 (trivial, single Q).
    """

```

**7. Iterative Implementation**

*Iteration 1: Skeleton with stubs*

```python
def solveNQueens(n: int):
    results = []
    
    # stubs
    def is_safe(r, c): return True
    def place_queen(r, c): pass
    def remove_queen(r, c): pass
    def format_board(): return []

    def backtrack(row):
        # Base case
        if row == n:
            results.append(format_board())
            return
        
        # Try all columns for current row
        for col in range(n):
            if is_safe(row, col):
                place_queen(row, col)
                backtrack(row + 1)
                remove_queen(row, col)

    backtrack(0)
    return results

```

*Iteration 2: Fleshing out state and helpers*

```python
def solveNQueens(n: int):
    results = []
    
    # State tracking
    cols = set()
    pos_diags = set() # r + c
    neg_diags = set() # r - c
    
    # Internal board representation
    board = [["."] * n for _ in range(n)] 

    # Implement helpers using state
    def is_safe(r, c):
        return c not in cols and (r + c) not in pos_diags and (r - c) not in neg_diags

    def place_queen(r, c):
        board[r][c] = "Q"
        cols.add(c)
        pos_diags.add(r + c)
        neg_diags.add(r - c)

    def remove_queen(r, c):
        board[r][c] = "."
        cols.remove(c)
        pos_diags.remove(r + c)
        neg_diags.remove(r - c)

    def format_board():
        return ["".join(row) for row in board]

    def backtrack(row):
        if row == n:
            results.append(format_board())
            return
        
        for col in range(n):
            if is_safe(row, col):
                place_queen(row, col)
                backtrack(row + 1)
                remove_queen(row, col) # backtrack step

    backtrack(0)
    return results

```

*Iteration 3: Addressing edge cases*
(Checking outline: `n=2` and `n=3` return empty naturally through loop exhaustion without reaching `row == n`. `n=1` works naturally. No specific code patches strictly required, algorithm handles invariants perfectly. To save runtime, we can add early returns for known impossible constraints.)

```python
def solveNQueens(n: int):
    # Edge case patch: Early exit for impossible boards
    if n == 2 or n == 3:
        return []

    results = []
    cols = set()
    pos_diags = set() 
    neg_diags = set() 
    board = [["."] * n for _ in range(n)] 

    def is_safe(r, c):
        return c not in cols and (r + c) not in pos_diags and (r - c) not in neg_diags

    def place_queen(r, c):
        board[r][c] = "Q"
        cols.add(c)
        pos_diags.add(r + c)
        neg_diags.add(r - c)

    def remove_queen(r, c):
        board[r][c] = "."
        cols.remove(c)
        pos_diags.remove(r + c)
        neg_diags.remove(r - c)

    def format_board():
        return ["".join(row) for row in board]

    def backtrack(row):
        if row == n:
            results.append(format_board())
            return
        
        for col in range(n):
            if is_safe(row, col):
                place_queen(row, col)
                backtrack(row + 1)
                remove_queen(row, col)

    backtrack(0)
    return results

```

**8. Complexity & Optimizations**

* **Time Complexity**: $O(N!)$. First row has $N$ options, second row $\le N-1$ options, etc. Sets provide $O(1)$ lookup, meaning validation step adds no overhead.
* **Space Complexity**: $O(N)$ auxiliary stack space. Board storage takes $O(N^2)$, overall sets take $O(N)$.
* **Optimization via Bitmasking**:
Sets have a small overhead. We can track `cols`, `pos_diags`, `neg_diags` using integers (bitmasks) where each bit represents a column or diagonal. Bitwise `AND`/`OR` operations evaluate in true constant time with less memory overhead than Python `set`. However, bitwise logic is hard to read/explain, violating our "prefer clear implementations" rule. The Set approach is the optimal balance of efficiency and readability.