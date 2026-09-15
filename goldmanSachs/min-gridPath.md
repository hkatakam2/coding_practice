### question

Given a m x n grid filled with non-negative numbers, find a path from top left to bottom right, which minimizes the sum of all numbers along its path.

Note: You can only move either down or right at any point in time.

 

Example 1:


Input: grid = [[1,3,1],[1,5,1],[4,2,1]]
Output: 7
Explanation: Because the path 1 → 3 → 1 → 1 → 1 minimizes the sum.
Example 2:

Input: grid = [[1,2,3],[4,5,6]]
Output: 12

## 1. Restate the problem

We have an `m x n` grid of non-negative numbers.

Start at the **top-left** cell and reach the **bottom-right** cell.

Allowed moves:

* right
* down

Return the **minimum possible sum of all cells visited**, including start and end.

---

## 2. Clarifying questions

In an interview, I would confirm:

* Can I assume `grid` is non-empty? → usually yes.
* Are all values non-negative? → yes.
* Can I move only right/down? → yes.
* Do we return the path or just its minimum sum? → just the sum.
* Can I modify the input grid? → worth asking because it enables `O(1)` extra space.

I'll first solve without modifying the input.

---

## 3. Work an example by hand

```text
grid =
[
  [1, 3, 1],
  [1, 5, 1],
  [4, 2, 1]
]
```

At each cell, the only ways to enter it are:

* from above
* from left

So minimum cost to reach a cell is:

```text
cell value + min(cost from above, cost from left)
```

Build minimum costs:

```text
1  4  5
2  7  6
6  8  7
```

Bottom-right = `7`.

Path:

```text
1 → 3 → 1 → 1 → 1
```

---

# 4. Brainstorm solutions

### Solution 1: brute-force recursion

From every cell:

```text
try going right
try going down
take the cheaper result
```

There can be exponentially many paths.

```text
Time:  O(2^(m+n))
Space: O(m+n) recursion depth
```

This directly matches how we solved it conceptually by hand, but repeats the same subproblems many times.

---

### Solution 2: recursion + memoization

Cache:

```text
minimum cost from this cell to destination
```

Every cell is computed once.

```text
Time:  O(m*n)
Space: O(m*n)
```

Good solution, but iterative DP is simpler here.

---

### Solution 3: 2D dynamic programming

Maintain:

```text
dp[row][col]
```

meaning:

> minimum path sum from top-left to this cell.

Transition:

```text
dp[row][col]
    = grid[row][col]
      + min(dp above, dp left)
```

```text
Time:  O(m*n)
Space: O(m*n)
```

Very clear interview solution.

---

### Solution 4: 1D dynamic programming

We don't actually need the entire DP table.

While processing one row, each cell only needs:

```text
minimum cost from above
minimum cost from left
```

A 1D array can maintain those.

```text
Time:  O(m*n)
Space: O(n)
```

I would probably implement this after explaining the 2D recurrence.

---

# 5. Selected solution

Start with **2D DP** because the recurrence is extremely easy to explain.

Key observation:

> Because movement is only right/down, any path reaching a cell must come from exactly one of two places: above or left.

That gives us optimal substructure.

---

# 6. Implementation outline

```python
def minPathSum(grid):  # -> int
    """
    Reframe:
    Minimum cost to reach a cell depends only on the cheaper
    minimum-cost path reaching its top or left neighbor.

    State:
    A DP table where each cell stores the minimum total cost
    required to reach that grid position from the start.

    Invariant:
    After processing a cell, its DP value is the minimum cost
    of every valid path from the top-left to that cell.

    minimumPreviousCost(top, left) =
    cheaper valid way of entering the current cell.

    Core logic:
    - initialize the starting cell with its own value
    - fill the first row using only the cell to the left
    - fill the first column using only the cell above
    - for every remaining cell:
        - choose the cheaper cost from above or left
        - add the current cell's value
    - return the cost stored for the bottom-right cell

    Edge cases:
    - grid contains only one cell
    - grid contains only one row
    - grid contains only one column
    - grid contains zero values
    """
```

---

# 7. Iterative implementation

## Iteration 1: skeleton

```python
def minPathSum(grid):
    rows = len(grid)
    cols = len(grid[0])

    dp = [[0] * cols for _ in range(rows)]

    # initialize starting position

    # initialize first row

    # initialize first column

    # process remaining cells

    # return bottom-right answer
```

---

## Iteration 2: initialize the obvious path boundaries

The top-left cell has no predecessor.

```python
dp[0][0] = grid[0][0]
```

For the first row, we cannot come from above.

```python
for col in range(1, cols):
    dp[0][col] = dp[0][col - 1] + grid[0][col]
```

For the first column, we cannot come from the left.

```python
for row in range(1, rows):
    dp[row][0] = dp[row - 1][0] + grid[row][0]
```

Code now:

```python
def minPathSum(grid):
    rows = len(grid)
    cols = len(grid[0])

    dp = [[0] * cols for _ in range(rows)]

    # Starting cell.
    dp[0][0] = grid[0][0]

    # Only possible movement along first row is right.
    for col in range(1, cols):
        dp[0][col] = dp[0][col - 1] + grid[0][col]

    # Only possible movement along first column is down.
    for row in range(1, rows):
        dp[row][0] = dp[row - 1][0] + grid[row][0]

    # TODO: remaining cells

    return dp[rows - 1][cols - 1]
```

---

## Iteration 3: implement the core recurrence

For an interior cell:

```text
best path =
current value
+
minimum(
    path reaching cell above,
    path reaching cell left
)
```

```python
for row in range(1, rows):
    for col in range(1, cols):
        dp[row][col] = (
            grid[row][col]
            + min(
                dp[row - 1][col],
                dp[row][col - 1]
            )
        )
```

Full implementation:

```python
def minPathSum(grid):
    rows = len(grid)
    cols = len(grid[0])

    dp = [[0] * cols for _ in range(rows)]

    dp[0][0] = grid[0][0]

    for col in range(1, cols):
        dp[0][col] = dp[0][col - 1] + grid[0][col]

    for row in range(1, rows):
        dp[row][0] = dp[row - 1][0] + grid[row][0]

    for row in range(1, rows):
        for col in range(1, cols):
            dp[row][col] = (
                grid[row][col]
                + min(
                    dp[row - 1][col],
                    dp[row][col - 1]
                )
            )

    return dp[rows - 1][cols - 1]
```

---

# 8. Walk the edge cases

### Single cell

```python
grid = [[5]]
```

We initialize:

```python
dp[0][0] = 5
```

Neither loop runs.

Returns:

```text
5
```

Works without changes.

---

### Single row

```python
[[1, 2, 3]]
```

Only first-row initialization runs:

```text
1 → 3 → 6
```

Returns `6`.

Works.

---

### Single column

```python
[
 [1],
 [2],
 [3]
]
```

First-column initialization gives:

```text
1
3
6
```

Works.

---

### Zero values

```python
[
 [0, 0],
 [0, 0]
]
```

DP naturally handles them.

No special handling required.

---

# 9. Complexity

We visit every cell once.

```text
Time: O(m*n)
```

The DP matrix stores one value per cell.

```text
Space: O(m*n)
```

---

# Follow-up optimization: O(n) space

Interviewer may ask:

> "Can you reduce the extra space?"

Yes.

When processing:

```python
dp[col]
```

before updating it represents the minimum cost **from above**.

And:

```python
dp[col - 1]
```

already represents the minimum cost **from the left**.

So:

```python
dp[col] = grid[row][col] + min(dp[col], dp[col - 1])
```

Implementation:

```python
def minPathSum(grid):
    rows = len(grid)
    cols = len(grid[0])

    dp = [0] * cols

    dp[0] = grid[0][0]

    # Build first row.
    for col in range(1, cols):
        dp[col] = dp[col - 1] + grid[0][col]

    for row in range(1, rows):
        # First column can only come from above.
        dp[0] += grid[row][0]

        for col in range(1, cols):
            dp[col] = (
                grid[row][col]
                + min(
                    dp[col],      # from above
                    dp[col - 1]   # from left
                )
            )

    return dp[-1]
```

```text
Time:  O(m*n)
Space: O(n)
```

The interview sentence to remember is:

> **"For every cell, there are only two possible predecessors—top and left—so the minimum cost to reach the current cell is its value plus the cheaper of those two previously computed minimum costs."**
