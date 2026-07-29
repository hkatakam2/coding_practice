### 1. Restate the problem

We have a grid of size `m` rows by `n` columns.
We start at the top-left cell `(0, 0)` and must reach the bottom-right cell `(m - 1, n - 1)`.
We can only move down or right.
We need to find the total number of unique paths to reach the destination.

### 2. Ask clarifying questions

* Are there any obstacles in the grid? (Assume no, based on the description).
* Can `m` or `n` be 0 or negative? (Assume `m >= 1` and `n >= 1`).
* Is time or space complexity prioritized? (Assume standard tradeoffs; $O(m \times n)$ time is expected, but space can be optimized).
* The problem guarantees the output fits in a 32-bit integer, so we don't need `long` or `BigInteger` for the final result. Do we need to worry about intermediate overflow? (Since path counts strictly increase and the max answer fits in 32 bits, intermediate additions will also fit in standard `int`).

### 3. Work through an example by hand

Let `m = 3` and `n = 2`.
Grid coordinates:
(0,0) (0,1)
(1,0) (1,1)
(2,0) (2,1)

Let's trace paths from (0,0) to (2,1).
Every cell in the top row (row 0) can only be reached by moving right. Ways = 1.
Every cell in the left column (col 0) can only be reached by moving down. Ways = 1.

Calculate remaining cells based on the rule: `ways(row, col) = ways(row - 1, col) + ways(row, col - 1)`

* Cell (1,1) = ways(0,1) + ways(1,0) = 1 + 1 = 2
* Cell (2,1) = ways(1,1) + ways(2,0) = 2 + 1 = 3

Total unique paths = 3.

### 4. Brainstorm solutions aloud

* **Recursive DFS:** Try every path moving right and down.
* Time: $O(2^{m+n})$ because we branch twice at every step.
* Space: $O(m + n)$ for the recursion stack.
* Verdict: Too slow.


* **Top-Down DP (Memoization):** Add a 2D cache to the DFS.
* Time: $O(m \times n)$.
* Space: $O(m \times n)$ for cache and stack.
* Verdict: Good, but recursion has overhead.


* **Bottom-Up DP (2D Tabulation):** Build an `m x n` matrix. Fill the first row and column with 1s. Traverse row by row.
* Time: $O(m \times n)$.
* Space: $O(m \times n)$.
* Verdict: Excellent, easy to understand.


* **Bottom-Up DP (1D Space Optimization):** Notice that calculating the current row only requires the values from the *immediately previous row*. We can use a single 1D array of size `n`.
* Time: $O(m \times n)$.
* Space: $O(n)$.
* Verdict: Optimal DP solution.


* **Combinatorics (Math):** To reach the end, we *must* make exactly `m - 1` Down moves and `n - 1` Right moves. Total moves = `(m - 1) + (n - 1)`. The answer is choosing `m - 1` positions for the Down moves from the total moves: $\binom{m+n-2}{m-1}$.
* Time: $O(m)$ or $O(n)$.
* Space: $O(1)$.
* Verdict: Most efficient, but requires careful division to avoid intermediate overflow or floating-point errors. Interviewers usually prefer the DP approach because it extends easily to follow-up questions (like adding obstacles).



### 5. Select the solution

I will implement the **Bottom-Up DP with 1D Space Optimization**.
It comfortably satisfies the constraints, is easy to explain, avoids mathematical edge cases with factorial combinations, and sets up perfectly for typical interview follow-ups. We will use a standard `int[]` array to track the state of the current row.

### 6. Write the implementation outline

```java
int uniquePaths(int m, int n) {
    /*
     * Reframe:
     * Calculate paths grid-cell by grid-cell. A cell's paths equal the paths 
     * from the cell above it plus the cell left of it.
     *
     * State:
     * A 1D integer array `row` of size n.
     * Chosen because calculating row `r` only requires data from row `r-1`.
     * We overwrite the array in-place to represent the new row.
     *
     * Invariant:
     * During computation of cell (r, c), `row[c]` holds the path count from the cell 
     * directly above, and `row[c-1]` holds the path count from the cell directly left.
     *
     * Core logic:
     * - Create an array of size n, filled with 1s (representing row 0).
     * - Loop through rows 1 to m-1.
     * - Loop through columns 1 to n-1.
     * - Update row[c] by adding row[c-1] to it.
     * - The final answer is at row[n-1].
     *
     * Edge cases:
     * - Grid is 1xN or Mx1 (requires 0 iterations, directly returns 1).
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton and standard 2D DP**
First, let's visualize the unoptimized 2D array approach. It maps directly to the grid.

```java
int uniquePaths(int m, int n) {
    int[][] dp = new int[m][n];

    // TODO: initialize top row and left column

    // TODO: iterate over remaining cells and sum upper and left cells

    return dp[m - 1][n - 1];
}

```

**Iteration 2: Complete the 2D DP**
We fill the grid iteratively.

```java
int uniquePaths(int m, int n) {
    int[][] dp = new int[m][n];

    // Added: Base cases. 1 path to anywhere in row 0 and col 0.
    for (int i = 0; i < m; i++) dp[i][0] = 1;
    for (int j = 0; j < n; j++) dp[0][j] = 1;

    // Added: Fill the rest of the table
    for (int i = 1; i < m; i++) {
        for (int j = 1; j < n; j++) {
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1];
        }
    }

    return dp[m - 1][n - 1];
}

```

**Iteration 3: Space Optimization to 1D DP**
We drop the `m` dimension. Notice `dp[i][j] = dp[i - 1][j] + dp[i][j - 1]`.
If we maintain a single array `row`, then before we update `row[j]`, it still contains the value from the previous row (`dp[i - 1][j]`). `row[j - 1]` has already been updated for the current row (`dp[i][j - 1]`).

```java
int uniquePaths(int m, int n) {
    // Changed: State is now a 1D array representing the current row.
    int[] row = new int[n];
    
    // Added: Initialize row 0. All cells in the top row have exactly 1 path.
    Arrays.fill(row, 1);

    for (int i = 1; i < m; i++) {
        for (int j = 1; j < n; j++) {
            // Changed: row[j] (value from above) + row[j - 1] (value from left)
            row[j] = row[j] + row[j - 1];
        }
    }

    return row[n - 1];
}

```

### 8. Edge-case walkthrough and patches

* **`m = 1` or `n = 1`:** If `m = 1`, the outer loop (`i < m`) never executes. `Arrays.fill` ensures `row` is all 1s, and we return `row[n - 1]`, which is 1. Correct. If `n = 1`, the inner loop (`j < n`) never executes, and we return `row[0]`, which is 1. Correct.
* **Overflow:** The problem states the result fits in a 32-bit integer. Because all additions are positive and strictly bounded by the final answer, no intermediate value can overflow an `int`. Correct.
* **Memory constraint:** If `n` is massive but `m` is small, we could use an array of size `m` instead to save space. We can add a quick swap at the beginning, but since `m` and `n` max out around 100 based on standard integer bounds for this problem, $O(n)$ space is already trivial. We'll stick to the simpler version for clarity.

### 9. Final code

```java
class Solution {
    public int uniquePaths(int m, int n) {
        int[] row = new int[n];
        
        // Base case: the entire top row has exactly 1 path to reach each cell.
        Arrays.fill(row, 1);

        // Process grid row by row, skipping the top row (index 0)
        for (int r = 1; r < m; r++) {
            // Process cell by cell, skipping the leftmost column (index 0)
            // which always stays 1.
            for (int c = 1; c < n; c++) {
                // row[c] currently holds the path count from the cell directly above.
                // row[c - 1] holds the path count from the cell directly to the left.
                row[c] += row[c - 1];
            }
        }

        // The final cell's value is the answer.
        return row[n - 1];
    }
}

```

### 10. Complexity

* **Time Complexity:** $O(m \times n)$. We iterate through the grid exactly once, performing a constant-time addition at each step.
* **Space Complexity:** $O(n)$. We only store a single 1D array of size `n`.

### 11. Brief test walkthrough

Input: `m = 3`, `n = 2`

1. `row` is created with size 2. `row = [1, 1]`.
2. Outer loop `r = 1` to 2:
* **r = 1:**
* `c = 1`: `row[1] = row[1] + row[0]` => `row[1] = 1 + 1 = 2`.
* Array is now `[1, 2]`.


* **r = 2:**
* `c = 1`: `row[1] = row[1] + row[0]` => `row[1] = 2 + 1 = 3`.
* Array is now `[1, 3]`.




3. Loop ends.
4. Return `row[1]`, which is `3`. Matches the expected result perfectly.