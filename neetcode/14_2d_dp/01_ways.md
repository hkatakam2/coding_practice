## question
There is an `m x n` grid where you are allowed to move either down or to the right at any point in time.
Given the two integers `m` and `n`, return the number of possible unique paths that can be taken from the top-left corner of the grid (`grid[0][0]`) to the bottom-right corner (`grid[m - 1][n - 1]`).
You may assume the output will fit in a 32-bit integer.

# Step 1 — Restate

Grid `m` rows × `n` cols. Start top-left, end bottom-right. Each move: right or down only. Count distinct paths.

# Step 2 — Clarifying questions

- `m, n >= 1`? (assume yes; a 1×1 grid = 1 path, you're already there)
- Any blocked cells? (no — that's a different problem)
- Output fits 32-bit, so no overflow handling needed.
- Inputs: two ints. Output: one int (count).

# Step 3 — Example by hand

`m=3, n=3` grid. Label cells by paths-to-reach. Top row + left col all = 1 (only one way: straight). Each inner cell = (from above) + (from left).

```
1  1  1
1  2  3
1  3  6
```

Answer = `6`.

# Step 4 — Brainstorm

- **Recursion (brute force):** `paths(r,c) = paths(r-1,c)+paths(r,c-1)`. Exponential, ~O(2^(m+n)). Clear but slow.
- **Recursion + memo:** cache `(r,c)`. O(m·n) time/space.
- **DP grid (the by-hand method from step 3):** fill table row by row. O(m·n) time, O(m·n) space — easy to explain.
- **DP 1-row:** keep only previous row. O(n) space.
- **Math (combinatorics):** total moves = `(m-1)+(n-1)`, choose which are downs → `C(m+n-2, m-1)`. O(min(m,n)) time, O(1) space. Cleverest, least obvious.

# Step 5 — Pick

I recommend the **DP grid** — it *is* the by-hand method from step 3, reads directly off the example, easy to explain. The math solution is elegant but harder to derive live.

Which do you want — DP grid, DP 1-row, or combinatorics?
# Step 6 — Outline

```python
def unique_paths(m, n):  # -> int
    """
    Reframe: paths-to-cell = paths-to-cell-above + paths-to-cell-left.
    State: 2D table `count`, count[r][c] = #ways to reach (r,c).
        chosen because each cell's answer depends only on its two
        already-solved neighbors (up, left) — clean subproblem overlap.
    Invariant: when we compute (r,c), (r-1,c) and (r,c-1) are final.

    fill_borders()        = top row & left col all set to 1 (one straight path).
    sum_neighbors(r,c)    = count above + count left.

    Core logic:
    - make table, every cell starts unknown
    - first row and first col = 1
    - for each remaining cell, in order, set it to sum_neighbors
    - answer = bottom-right cell
    Edge cases:
    - single row or single col -> answer 1 (borders already cover it)
    - 1x1 grid -> answer 1
    """
```

# Step 7 — Iterative implementation

**Iteration 1 — skeleton from the plain English:**

```python
def unique_paths(m, n):
    count = make_table(m, n)        # TODO: m x n, zeros
    fill_borders(count)             # TODO: top row + left col = 1
    for r, c in inner_cells():      # TODO: r in 1..m-1, c in 1..n-1
        count[r][c] = sum_neighbors(count, r, c)  # TODO
    return count[m-1][n-1]
```

**Iteration 2 — table + sum_neighbors (the easy concrete bits):**

```python
def unique_paths(m, n):
    count = [[0] * n for _ in range(m)]   # m x n grid of zeros
    fill_borders(count)                   # still TODO
    for r in range(1, m):                 # inner cells, skip row 0 & col 0
        for c in range(1, n):
            count[r][c] = count[r-1][c] + count[r][c-1]   # above + left
    return count[m-1][n-1]
```

**Iteration 3 — inline the borders, drop last helper:**

```python
def unique_paths(m, n):
    count = [[0] * n for _ in range(m)]
    for r in range(m):
        count[r][0] = 1           # left col: one way down
    for c in range(n):
        count[0][c] = 1           # top row: one way right
    for r in range(1, m):
        for c in range(1, n):
            count[r][c] = count[r-1][c] + count[r][c-1]
    return count[m-1][n-1]
```

Core logic complete.

**Edge cases walk:**
- *Single row (`m=1`):* inner loop never runs (`range(1,1)` empty), top row set to 1, returns `count[0][n-1]=1`. ✓ no patch.
- *Single col (`n=1`):* symmetric, returns 1. ✓
- *1×1:* both borders set `count[0][0]=1`, returns 1. ✓

No patches needed — borders absorb every edge.

# Step 8 — Complexity

- Time: `O(m·n)` — visit each cell once, O(1) work per cell.
- Space: `O(m·n)` for the table.

**Optimization (optional):** each cell only needs the previous row, so collapse to one 1D array → `O(n)` space:

```python
def unique_paths(m, n):
    row = [1] * n                 # represents top row (all 1s)
    for _ in range(1, m):
        for c in range(1, n):
            row[c] += row[c-1]    # new = old(above) + left(already updated)
    return row[-1]
```

Same O(m·n) time, drops space to O(min by swapping to shorter dim if desired).